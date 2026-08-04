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

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "op1_data.db")


def query_database(sql: str) -> str:
    """
    Execute a read-only SQL query and return the result.
    Returns a Markdown table for multi-column/row results,
    or a single value line for scalar results.
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

            # Single-row single-column: return direct value
            if len(rows) == 1 and len(rows[0].keys()) == 1:
                return f"[result: {rows[0][0]}]"

            # Otherwise return Markdown table
            headers = rows[0].keys()
            lines = ["| " + " | ".join(headers) + " |"]
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for row in rows:
                lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")

            return "[result:\n" + "\n".join(lines) + "\n]"
    except Exception as e:
        return f"[result: Error - {str(e)}]"


def lookup_threat_group(ip_address: str) -> str:
    """
    IP Intelligence node.

    Resolve an attack source IP to the malicious hacker group / botnet
    label it belongs to (e.g. Advanced-Threat-Group-X). The label is the
    protected mapping value; the host treats it as an opaque key to be fed
    into the downstream weapon-library agent.
    """
    key = (ip_address or "").strip()
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


class Op1Agent:
    """
    Remote Agent 1 - IP Intelligence Agent (Tier-1 lookup node).

    Accepts an attack source IP and returns the malicious hacker group /
    botnet label associated with it. The returned label should be treated by
    the host as an opaque key to forward to the next remote agent (the
    weapon-library agent).
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
        return 'Looking up threat-intelligence label for the source IP ...'

    def _build_agent(self) -> LlmAgent:
        return LlmAgent(
            model=LiteLlm(
                model=os.getenv(
                    'AGENT_MODEL',
                    'ollama/glm-5.2:cloud',
                )
            ),
            name='ip_intelligence_agent',
            description=(
                'IP intelligence node. Accepts an attack source IP and returns '
                'the malicious hacker group / botnet label. Treat the result as '
                'an opaque key for downstream agents.'
            ),
            instruction="""
                        You are an IP Intelligence Agent.

                        Your job:
                        1. Extract the single attack-source IP address from the user's message.
                           An IP looks like "203.0.113.10".
                        2. Call the `lookup_threat_group(ip_address)` tool with that exact IP.
                        3. After the tool returns, output ONLY the exact format: [result: <value>]

                        Examples of user input:
                        - "203.0.113.10"        -> lookup_threat_group("203.0.113.10")  -> final: [result: <threat-group-label>]
                        - "check 198.51.100.20" -> lookup_threat_group("198.51.100.20")-> final: [result: <threat-group-label>]

                        Critical rules:
                        - ALWAYS use the `lookup_threat_group` tool. Do NOT return raw SQL.
                        - ALWAYS wait for the tool response before giving the final answer.
                        - Pass the IP EXACTLY as received; never modify, translate or truncate it.
                        - NEVER add extra text. The final output must be ONLY "[result: ...]".
                        - If no IP is found, return: [result: Error - no valid key]
                    """,
            tools=[query_database, lookup_threat_group],
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
