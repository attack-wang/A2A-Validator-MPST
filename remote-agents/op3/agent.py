import sqlite3
import os
import logging
from typing import Any
from collections.abc import AsyncIterable
from contextlib import closing

from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "op3_data.db")


def query_database(sql: str) -> str:
    """
    Execute a read-only SQL query and return the result.
    """
    try:
        cleaned = sql.strip().upper()
        if not cleaned.startswith("SELECT"):
            return "[result: Error - Only SELECT queries are allowed.]"

        with closing(sqlite3.connect(DB_PATH)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            if not rows:
                return "[result: Not Found]"

            if len(rows) == 1 and len(rows[0].keys()) == 1:
                return f"[result: {rows[0][0]}]"

            headers = rows[0].keys()
            lines = ["| " + " | ".join(headers) + " |"]
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for row in rows:
                lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")

            return "[result:\n" + "\n".join(lines) + "\n]"
    except Exception as e:
        return f"[result: Error - {str(e)}]"


def lookup_defense_strategy(cve_id: str) -> str:
    """
    Defense-Strategy node.

    Given a CVE ID (e.g. CVE-2026-9999), resolve it to the security
    patch / firewall rule script that the interception system should
    auto-deploy (e.g. Block_Rule_Protocol_v3.sh). The script name is the
    protected mapping value; it is the final result returned to the user.
    """
    key = (cve_id or "").strip()
    if not key:
        return "[result: Error - no valid key]"

    sql = """
        SELECT m.value
        FROM mapping m
        WHERE m.key = ?
        LIMIT 1
    """
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(sql, (key,))
            row = cur.fetchone()
            if not row:
                return "[result: Not Found]"
            return f"[result: {row['value']}]"
    except Exception as e:
        return f"[result: Error - {str(e)}]"


class Op3Agent:
    """
    Remote Agent 3 - Defense-Strategy Agent (Tier-3 lookup node, terminal).

    Accepts a CVE ID and returns the security patch / firewall rule script
    the interception system should auto-deploy. The returned script name is
    the final result delivered back to the user; there is no further
    downstream agent.
    """

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']
    requires_tool_call = True

    def __init__(self):
        self._agent = self._build_agent()
        self._user_id = 'remote_agent'
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    def get_processing_message(self) -> str:
        return 'Looking up the auto-deploy defense rule for the CVE ...'

    def _build_agent(self) -> LlmAgent:
        return LlmAgent(
            model=LiteLlm(
                model=os.getenv(
                    'AGENT_MODEL',
                    'ollama/glm-5.2:cloud',
                )
            ),
            name='defense_strategy_agent',
            description=(
                'Defense-strategy node. Accepts a CVE ID and returns the '
                'security patch / firewall rule script the interception system '
                'should auto-deploy. This is the terminal node of the chain.'
            ),
            instruction="""
                        You are a Defense-Strategy Agent.

                        Your job:
                        1. Extract the single CVE ID from the user's message.
                           A CVE ID looks like "CVE-2026-9999".
                        2. Call the `lookup_defense_strategy(cve_id)` tool with that exact CVE ID.
                        3. After the tool returns, output ONLY the exact format: [result: <value>]

                        Examples of user input:
                        - "CVE-2026-9999"          -> lookup_defense_strategy("CVE-2026-9999") -> final: [result: <defense-script>]
                        - "patch for CVE-2026-9001" -> lookup_defense_strategy("CVE-2026-9001") -> final: [result: <defense-script>]

                        Critical rules:
                        - ALWAYS use the `lookup_defense_strategy` tool. Do NOT return raw SQL.
                        - ALWAYS wait for the tool response before giving the final answer.
                        - Pass the CVE ID EXACTLY as received; never modify, translate or truncate it.
                        - NEVER add extra text. The final output must be ONLY "[result: ...]".
                        - If no CVE ID is found, return: [result: Error - no valid key]
                    """,
            tools=[query_database, lookup_defense_strategy],
        )

    async def stream(self, query, session_id) -> AsyncIterable[dict[str, Any]]:
        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )

        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state={},
                session_id=session_id,
            )

        content = types.Content(
            role='user', parts=[types.Part.from_text(text=query)]
        )

        tool_call_observed = False
        tool_response_observed = False
        last_tool_name = ''
        async for event in self._runner.run_async(
                user_id=self._user_id, session_id=session.id, new_message=content
        ):
            parts = event.content.parts if event.content and event.content.parts else []
            final_event_has_tool_call = False
            for part in parts:
                function_call = getattr(part, 'function_call', None)
                if function_call:
                    tool_call_observed = True
                    final_event_has_tool_call = event.is_final_response()
                    last_tool_name = getattr(function_call, 'name', '') or last_tool_name
                if getattr(part, 'function_response', None):
                    tool_response_observed = True

            if event.is_final_response():
                response = ''
                if (
                        event.content and event.content.parts and event.content.parts[0].text
                ):
                    response = '\n'.join([p.text for p in event.content.parts if p.text])
                elif (
                        event.content and event.content.parts and
                        any([True for p in event.content.parts if p.function_response])
                ):
                    function_response = next(
                        p.function_response for p in event.content.parts if p.function_response
                    )
                    response = function_response.result
                elif (
                        event.content and event.content.parts and
                        any([True for p in event.content.parts if p.function_call])
                ):
                    function_call = next(
                        p.function_call for p in event.content.parts if p.function_call
                    )
                    response = f"Error: Tool call not executed - {function_call.name}"

                yield {
                    'is_task_complete': True,
                    'content': response,
                    'tool_required': True,
                    'tool_call_observed': tool_call_observed,
                    'tool_response_observed': tool_response_observed,
                    'unexecuted_tool_call': final_event_has_tool_call,
                    'tool_name': last_tool_name,
                }
            else:
                yield {
                    'is_task_complete': False,
                    'updates': self.get_processing_message(),
                }
