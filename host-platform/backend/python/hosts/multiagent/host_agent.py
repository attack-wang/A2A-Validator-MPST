import asyncio
import base64
import json
import logging
import os
import uuid

from typing import Any

import httpx

from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import (
    AgentCard,
    DataPart,
    Message,
    Part,
    Role,
    Task,
    TaskState,
    TextPart,
    TransportProtocol,
)
from google.adk import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from gt_projection import GTProjection
from host_communication_logging import log_a2a_communication
from host_mpst_monitor import HostProtocolMonitor
from host_validation_logging import log_host_validation_error
from mpst_ext import resolve_validation_enabled
from remote_agent_connection import RemoteAgentConnections, TaskUpdateCallback
from timestamp_ext import TimestampExtension


logger = logging.getLogger(__name__)


class HostAgent:
    """The host agent.

    This is the agent responsible for choosing which remote agents to send
    tasks to and coordinate their work.
    """

    def __init__(
        self,
        remote_agent_addresses: list[str],
        http_client: httpx.AsyncClient,
        task_callback: TaskUpdateCallback | None = None,
        projection_method: str = "subset",
        validation_enabled: bool | None = None,
    ):
        self.task_callback = task_callback
        self.httpx_client = http_client
        self.validation_enabled = resolve_validation_enabled(
            validation_enabled
        )
        self.timestamp_extension = TimestampExtension()
        self.gt_projection = GTProjection(projection_method)
        self.host_protocol_monitor = HostProtocolMonitor()
        self._protocol_initialized_agents: set[str] = set()
        self._default_gt_file = os.getenv(
            "MPST_DEFAULT_GT_FILE",
            "Travel.gt",
        )
        self._default_protocol_name = os.getenv(
            "MPST_DEFAULT_PROTOCOL_NAME",
            "Travel",
        )
        config = ClientConfig(
            httpx_client=self.httpx_client,
            supported_transports=[
                TransportProtocol.jsonrpc,
                TransportProtocol.http_json,
            ],
        )
        client_factory = ClientFactory(config)
        client_factory = self.timestamp_extension.wrap_client_factory(
            client_factory
        )
        self.client_factory = client_factory
        self.remote_agent_connections: dict[str, RemoteAgentConnections] = {}
        self.cards: dict[str, AgentCard] = {}
        self.agents: str = ''
        self.predefined_workflows = self._load_predefined_workflows()
        self._background_tasks: set[asyncio.Task] = set()
        logger.info(
            "[VALIDATION MODE] role=Host enabled=%s",
            self.validation_enabled,
        )
        if remote_agent_addresses:
            loop = asyncio.get_running_loop()
            task = loop.create_task(
                self.init_remote_agent_addresses(remote_agent_addresses)
            )
            self._background_tasks.add(task)
            task.add_done_callback(self._background_tasks.discard)

    async def shutdown(self):
        """Clean up background tasks gracefully."""
        for task in self._background_tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    @staticmethod
    def _agent_name_to_role(agent_name: str) -> str:
        """Map AgentCard display name to protocol role name."""
        mapping = {
            "weather agent": "Weatheragent",
            "guide agent": "Guideagent",
            "transport select agent": "Transportselectagent",
            "train agent": "Trainagent",
            "flight agent": "Flightagent",
            "hotel agent": "Hotelagent",
            "ticket agent": "Ticketagent",
            "public transport agent": "Publictransportagent",
            "budget agent": "Budgetagent",
            "ip intelligence agent": "OP1",
            "weapon library asset agent": "OP2",
            "defense strategy agent": "OP3",
        }
        return mapping.get(agent_name.strip().lower(), agent_name.replace(" ", "").replace("_", ""))

    @staticmethod
    def _normalize_agent_identifier(agent_name: str) -> str:
        """Normalize display names and protocol roles for alias matching."""
        return ''.join(
            character
            for character in agent_name.strip().lower()
            if character.isalnum()
        )

    def _resolve_agent_name(self, agent_name: str) -> str:
        """Resolve an AgentCard display name from a display/role-style alias."""
        if agent_name in self.remote_agent_connections:
            return agent_name
        requested = self._normalize_agent_identifier(agent_name)
        for registered_name in self.remote_agent_connections:
            aliases = {
                self._normalize_agent_identifier(registered_name),
                self._normalize_agent_identifier(
                    self._agent_name_to_role(registered_name)
                ),
            }
            if requested in aliases:
                if registered_name != agent_name:
                    logger.info(
                        "[AGENT ALIAS] Resolved %r to registered agent %r",
                        agent_name,
                        registered_name,
                    )
                return registered_name
        return agent_name

    def _is_protocol_initialized(self, agent_name: str) -> bool:
        return agent_name in self._protocol_initialized_agents

    def _mark_protocol_initialized(self, agent_name: str):
        self._protocol_initialized_agents.add(agent_name)
        logger.info(f"[MPST] Protocol initialized for agent: {agent_name}")

    def _load_predefined_workflows(self) -> dict[str, dict[str, Any]]:
        """Load predefined workflows from JSON file, fallback to env linear workflows."""
        workflow_file = os.getenv(
            'HOST_AGENT_WORKFLOW_FILE',
            os.path.join(os.path.dirname(__file__), 'workflows.json'),
        )
        if os.path.exists(workflow_file):
            with open(workflow_file, encoding='utf-8') as f:
                loaded = json.load(f)
            workflows = loaded.get('workflows', {})
            if workflows:
                return workflows

        # Backward compatible: linear workflows from env
        workflows_str = os.getenv('HOST_AGENT_WORKFLOWS', '').strip()
        linear_workflows: dict[str, dict[str, Any]] = {}
        if workflows_str:
            for item in workflows_str.split(';'):
                item = item.strip()
                if not item or ':' not in item:
                    continue
                workflow_name, steps_str = item.split(':', maxsplit=1)
                agent_steps = [s.strip() for s in steps_str.split('>') if s.strip()]
                if not workflow_name.strip() or not agent_steps:
                    continue
                nodes = []
                for i, agent_name in enumerate(agent_steps):
                    node_id = f'step_{i + 1}'
                    next_ids = [f'step_{i + 2}'] if i + 1 < len(agent_steps) else []
                    nodes.append(
                        {
                            'id': node_id,
                            'agent': agent_name,
                            'next': next_ids,
                        }
                    )
                linear_workflows[workflow_name.strip()] = {
                    'start': 'step_1',
                    'steps': nodes,
                }
        if linear_workflows:
            return linear_workflows
        return {}

    async def init_remote_agent_addresses(
        self, remote_agent_addresses: list[str]
    ):
        async with asyncio.TaskGroup() as task_group:
            for address in remote_agent_addresses:
                task_group.create_task(self.retrieve_card(address))
        # The task groups run in the background and complete.
        # Once completed the self.agents string is set and the remote
        # connections are established.

    async def retrieve_card(self, address: str):
        card_resolver = A2ACardResolver(self.httpx_client, address)
        card = await card_resolver.get_agent_card()
        self.register_agent_card(card)

    def register_agent_card(self, card: AgentCard):
        remote_connection = RemoteAgentConnections(self.client_factory, card)
        self.remote_agent_connections[card.name] = remote_connection
        self.cards[card.name] = card
        agent_info = []
        for ra in self.list_remote_agents():
            agent_info.append(json.dumps(ra))
        self.agents = '\n'.join(agent_info)

    def create_agent(self) -> Agent:
        # LITELLM_MODEL = os.getenv(
        #     'LITELLM_MODEL', 'gemini/gemini-2.5-flash-lite'


        # )
        return Agent(
            model=LiteLlm(
                model=os.getenv(
                    'HOST_MODEL',
                    'ollama/kimi-k2.6:cloud',
                )
            ),
            name='host_agent',
            instruction=self.root_instruction,
            before_model_callback=self.before_model_callback,
            description=(
                'This agent orchestrates the decomposition of the user request into'
                ' tasks that can be performed by the child agents.'
            ),
            tools=[
                self.list_remote_agents,
                self.send_message,
                self.list_gt_protocols,
                self.read_gt_protocol,
                self.project_gt_protocol,
                self.send_local_protocol,
                self.finalize_protocol,
            ],
        )

    def root_instruction(self, context: ReadonlyContext) -> str:
        current_agent = self.check_state(context)
        if self.validation_enabled:
            protocol_execution_instruction = f"""
Validation is enabled.
- The active protocol is `{self._default_gt_file}` with identifier
  `{self._default_protocol_name}`.
- `send_message` automatically projects and installs the matching local
  protocol before an agent's first business message. Do not call
  `send_local_protocol` separately unless the user explicitly asks to inspect
  protocol initialization.
- Follow the legal Host order and branch in the active global protocol.
- Before returning the final answer, call `finalize_protocol`. If it reports
  an incomplete protocol, continue the required agent interactions.
"""
        else:
            protocol_execution_instruction = """
Validation is disabled for the baseline condition.
- Do not call `send_local_protocol`, `project_gt_protocol`, or
  `finalize_protocol`.
- Send the same business requests directly with `send_message`.
- Do not add protocol labels or protocol-initialization turns.
"""
        return f"""You are an expert delegator that can delegate the user request to the
appropriate remote agents.

Discovery:
- Use `list_remote_agents` to see which remote agents exist and what they do.


Protocol Management (Global Types):
- Use `list_gt_protocols` to list all Global Type files (.gt) in the protocols directory.
  This shows all available protocol definitions for agent interactions.
- Use `read_gt_protocol` to read and parse Global Type files (.gt)
  from the protocols directory. This tool extracts processes/roles from the file.
- Use `project_gt_protocol` to project a global type into a local
  protocol for a specific role. This generates a role-specific view of the protocol
  that agents can use to understand their responsibilities. Usage:
  `project_gt_protocol(file_name, protocol_name, role)` where protocol_name is
  the protocol identifier and role is the target role (e.g., 'Host', 'OP1').
- Use `send_local_protocol` to send a projected local protocol to a remote agent.
  This initializes the Runtime Monitor on the remote agent side. Usage:
  `send_local_protocol(agent_name, file_name, protocol_name, role)` where agent_name
  is the target remote agent, file_name is the .gt file, protocol_name is the
  protocol identifier, and role is the role to project for that agent.

Execution:
- Runtime mode instructions:
{protocol_execution_instruction}
- Use `send_message` to talk to remote agents. You may call it multiple times, retry,
  or change strategy; message content and whether to pass prior results are your choice.
- Send the real business payload required by the target agent. Protocol labels
  are added and checked by the runtime; do not invent a generic `[number: ...]`
  or `[result: ...]` wrapper.
- You MUST actually execute `send_message` when action is needed, not only describe it.
- Wait for tool results before treating a step as done.
- Do not expose raw tool call syntax as the final user-facing answer.

CRITICAL RULES:
- When you decide to call a tool (like send_message), output ONLY the tool call with its arguments.
- The system (ADK framework) will automatically execute the tool and return the REAL result to you.
- You MUST NOT output fake tool results like "Tool Calls:" or "User:" pretending a tool was executed.
- You MUST NOT imagine or simulate what the tool would return. Wait for the actual result.
- If a tool returns nothing or fails, report that honestly instead of making up a response.
- Each workflow step requires a separate send_message call. Do not combine steps in one call.
Please rely on tools, and don't invent remote outputs. If information is missing, ask the user.
Focus on the most recent parts of the conversation.

Agents:
{self.agents}

Current agent: {current_agent['active_agent']}
"""

    def check_state(self, context: ReadonlyContext):
        state = context.state
        if (
            'context_id' in state
            and 'session_active' in state
            and state['session_active']
            and 'agent' in state
        ):
            return {'active_agent': f'{state["agent"]}'}
        return {'active_agent': 'None'}

    def before_model_callback(
        self, callback_context: CallbackContext, llm_request
    ):
        state = callback_context.state
        if 'session_active' not in state or not state['session_active']:
            state['session_active'] = True

    def list_remote_agents(self):
        """List the available remote agents you can use to delegate the task."""
        if not self.remote_agent_connections:
            return []

        remote_agent_info = []
        for card in self.cards.values():
            remote_agent_info.append(
                {'name': card.name, 'description': card.description}
            )
        return remote_agent_info

    def list_predefined_workflows(self):
        """Return workflow definitions from workflows.json (reference for the model).

        Structure: workflow name -> {{ start, steps: [{{ id, agent, next }}] }}.
        The host does not enforce this graph; use it to plan calls to `send_message`.
        """
        if not self.predefined_workflows:
            return {}
        return self.predefined_workflows

    def read_gt_protocol(self, file_name: str):
        """Read and parse a Global Type file from the protocols directory.

        This tool reads the content of a Global Type file (.gt) from the
        protocols directory and returns its contents along with a summary of the
        processes/roles defined within it.

        Args:
            file_name: The name of the Global Type file (e.g.,
                      'operation.gt')

        Returns:
            A dictionary containing:
            - file_name: The name of the file
            - file_path: The full path to the file
            - summary: A summary containing:
                - processes: List of processes/roles defined in the global type
                - content_preview: A preview of the file content
            - content_preview: A preview of the file content
            - full_content: The full content of the file
            - error: Error message if the file cannot be read
        """
        protocols_dir = os.path.join(os.path.dirname(__file__), "protocols")
        file_path = os.path.join(protocols_dir, file_name)
        
        result = self.gt_projection.read_protocol_file(file_path)

        if result.get("exists") and result.get("content"):
            summary = self.gt_projection.get_protocol_summary(result["content"])
            result["summary"] = summary

        if result.get("error"):
            return {
                "status": "error",
                "message": result["error"]
            }

        return {
            "status": "success",
            "file_name": result.get("file_name"),
            "file_path": result.get("file_path"),
            "summary": result.get("summary"),
            "content_preview": result.get("content", "")[:500] + "..." if len(result.get("content", "")) > 500 else result.get("content", ""),
            "full_content": result.get("content")
        }

    def list_gt_protocols(self):
        """List all Global Type files in the protocols directory.

        This tool lists all .gt files in the protocols directory, which
        contains the Global Type definitions for agent interactions.

        Returns:
            A list of protocol files with their names and paths.
        """
        protocols_dir = os.path.join(os.path.dirname(__file__), "protocols")
        if not os.path.exists(protocols_dir):
            os.makedirs(protocols_dir)
        
        protocols = self.gt_projection.list_protocols_in_directory(protocols_dir)
        
        if not protocols:
            return {
                "status": "empty",
                "message": "No Global Type files (.gt) found in the protocols directory"
            }
        
        return {
            "status": "success",
            "protocols": protocols
        }

    def project_gt_protocol(self, file_name: str, protocol_name: str, role: str):
        """Project a Global Type file for a specific role.

        This tool projects a global type file (.gt) into a local protocol
        for a specific role, which can be used by agents to understand their
        responsibilities in the protocol.

        Args:
            file_name: The name of the Global Type file (e.g.,
                      'operation.gt')
            protocol_name: The name/identifier of the protocol (used for reference)
            role: The role to project the protocol for (e.g., 'Host', 'OP1')

        Returns:
            A dictionary containing:
            - file_name: The name of the file
            - protocol_name: The name/identifier of the projected protocol
            - role: The role the protocol was projected for
            - local_protocol: The generated local protocol
            - successful_method: The projection method used (subset/classical)
            - error: Error message if projection failed
        """
        protocols_dir = os.path.join(os.path.dirname(__file__), "protocols")
        file_path = os.path.join(protocols_dir, file_name)
        
        result = self.gt_projection.project_protocol(file_path, protocol_name, role)

        if result.get("error"):
            return {
                "status": "error",
                "message": result["error"]
            }

        return {
            "status": "success",
            "file_name": file_name,
            "protocol_name": protocol_name,
            "role": role,
            "local_protocol": result.get("local_protocol"),
            "successful_method": result.get("successful_method")
        }

    async def send_local_protocol(
        self,
        agent_name: str,
        file_name: str,
        protocol_name: str,
        role: str,
        tool_context: ToolContext,
    ):
        """Send a local Scribble protocol to a remote agent.

        This method projects a global Scribble protocol for a specific role
        and sends the resulting local protocol to the target remote agent.
        The remote agent will use this to initialize its Runtime Monitor.

        Args:
            agent_name: The name of the remote agent to send the protocol to.
            file_name: The name of the Scribble protocol file.
            protocol_name: The name of the global protocol to project.
            role: The role to project the protocol for (should match the remote agent's role).
            tool_context: The tool context this method runs in.

        Returns:
            A dictionary containing the result of the operation.

        Raises:
            ValueError: If the agent is not found or the projection fails.
        """
        agent_name = self._resolve_agent_name(agent_name)
        state = tool_context.state
        if not self.validation_enabled:
            logger.info(
                "[VALIDATION DISABLED] Skip protocol setup for %s",
                agent_name,
            )
            return {
                "status": "success",
                "code": "ValidationDisabled",
                "message": (
                    "Protocol setup skipped because validation is disabled"
                ),
                "agent": agent_name,
                "protocol_name": protocol_name,
                "role": role,
                "validation_enabled": False,
            }

        # Session-level deduplication for send_local_protocol
        session_initialized = state.get('_mpst_initialized_agents', set())
        if agent_name in session_initialized:
            logger.info(f"[MPST] Dedup: skip send_local_protocol for {agent_name} (already in session)")
            return {
                "status": "success",
                "message": f"Protocol already initialized for {agent_name} in this session",
                "agent": agent_name,
            }
        if agent_name in self._protocol_initialized_agents:
            logger.info(f"[MPST] Dedup: skip send_local_protocol for {agent_name} (already initialized globally)")
            return {
                "status": "success",
                "message": f"Protocol already initialized for {agent_name}",
                "agent": agent_name,
            }

        # First, check if the agent exists
        if agent_name not in self.remote_agent_connections:
            return {
                "status": "error",
                "message": f"Agent {agent_name} not found. Available agents: {list(self.remote_agent_connections.keys())}"
            }

        # Project the protocol
        projection_result = self.project_gt_protocol(file_name, protocol_name, role)

        if projection_result.get("status") != "success":
            return {
                "status": "error",
                "message": f"Failed to project protocol: {projection_result.get('message', 'Unknown error')}"
            }

        local_protocol = projection_result.get("local_protocol")
        if not local_protocol:
            return {
                "status": "error",
                "message": "No local protocol generated from projection"
            }

        # Project for Host role and load into Host-side monitor (only on first init)
        if not self.host_protocol_monitor.initialized:
            host_projection = self.project_gt_protocol(file_name, protocol_name, "Host")
            if host_projection.get("status") == "success":
                host_local = host_projection.get("local_protocol")
                if host_local:
                    self.host_protocol_monitor.load_from_local_protocol(host_local, protocol_name)
            else:
                logger.warning(f"Host local projection failed: {host_projection.get('message')}")

        # Prepare the protocol setup message
        protocol_setup_message = {
            "type": "protocol_setup",
            "local_protocol": local_protocol,
            "role": role,
            "protocol_name": protocol_name,
            "file_name": file_name,
        }

        # Send the protocol to the remote agent
        state = tool_context.state
        state['agent'] = agent_name
        client = self.remote_agent_connections[agent_name]

        task_id = state.get('task_id', None)
        context_id = state.get('context_id', None)
        message_id = state.get('message_id', None)
        if not message_id:
            message_id = str(uuid.uuid4())

        request_message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text=json.dumps(protocol_setup_message)))],
            message_id=message_id,
            context_id=context_id,
            task_id=task_id,
        )

        try:
            log_a2a_communication(
                direction="outgoing",
                phase="protocol_setup",
                peer=agent_name,
                context_id=context_id,
                task_id=task_id,
                message_id=message_id,
                payload=request_message,
            )
            response = await client.send_message(request_message)
            log_a2a_communication(
                direction="incoming",
                phase="protocol_setup",
                peer=agent_name,
                context_id=context_id,
                task_id=task_id,
                message_id=message_id,
                payload=response,
            )

            # Check if the remote agent successfully initialized the protocol
            if isinstance(response, Task):
                if response.status.state == TaskState.completed:
                    self._mark_protocol_initialized(agent_name)
                    session_initialized = state.get('_mpst_initialized_agents', set())
                    session_initialized.add(agent_name)
                    state['_mpst_initialized_agents'] = session_initialized
                    return {
                        "status": "success",
                        "message": f"Local protocol sent to {agent_name} successfully",
                        "agent": agent_name,
                        "protocol_name": protocol_name,
                        "role": role,
                        "remote_response": response.status.message.parts[0].root.text if response.status.message and response.status.message.parts else "No response text"
                    }
                elif response.status.state == TaskState.failed:
                    return {
                        "status": "error",
                        "message": f"Remote agent failed to initialize protocol: {response.status.message.parts[0].root.text if response.status.message and response.status.message.parts else 'Unknown error'}"
                    }
                else:
                    return {
                        "status": "pending",
                        "message": f"Protocol setup in progress, state: {response.status.state}",
                        "agent": agent_name,
                    }
            elif isinstance(response, Message):
                return {
                    "status": "success",
                    "message": f"Local protocol sent to {agent_name}",
                    "agent": agent_name,
                    "protocol_name": protocol_name,
                    "role": role,
                    "remote_response": response.parts[0].root.text if response.parts else "No response"
                }
            else:
                return {
                    "status": "unknown",
                    "message": f"Unexpected response type: {type(response)}",
                    "agent": agent_name,
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to send protocol to {agent_name}: {str(e)}"
            }

    async def send_message(
        self, agent_name: str, message: str, tool_context: ToolContext
    ):
        """Sends a task either streaming (if supported) or non-streaming.

        This will send a message to the remote agent named agent_name.

        Args:
          agent_name: The name of the agent to send the task to.
          message: The message to send to the agent for the task.
          tool_context: The tool context this method runs in.

        Yields:
          A dictionary of JSON data.
        """
        requested_agent_name = agent_name
        agent_name = self._resolve_agent_name(agent_name)
        logger.info(
            "[SEND_MESSAGE] Called with agent=%s resolved_agent=%s message=%s...",
            requested_agent_name,
            agent_name,
            message[:80],
        )
        if agent_name not in self.remote_agent_connections:
            raise ValueError(f'Agent {agent_name} not found')
        state = tool_context.state
        state['agent'] = agent_name
        client = self.remote_agent_connections[agent_name]
        if not client:
            raise ValueError(f'Client not available for {agent_name}')
        protocol_session_id = ''
        if self.validation_enabled:
            protocol_session_id = state.setdefault(
                '_mpst_session_id',
                str(uuid.uuid4()),
            )
        task_id = state.get('task_id', None)
        context_id = state.get('context_id', None)
        message_id = state.get('message_id', None)
        task: Task
        if not message_id:
            message_id = str(uuid.uuid4())

        role = self._agent_name_to_role(agent_name)
        protocol_message = message
        if self.validation_enabled:
            # 自动协议初始化兜底（session 级别 + 实例级别双重防重）
            session_initialized = state.get(
                '_mpst_initialized_agents',
                set(),
            )
            if (
                agent_name not in session_initialized
                and agent_name not in self._protocol_initialized_agents
            ):
                logger.info(
                    "[MPST] Auto-init protocol for %s (role=%s)",
                    agent_name,
                    role,
                )
                try:
                    init_result = await self.send_local_protocol(
                        agent_name,
                        self._default_gt_file,
                        self._default_protocol_name,
                        role,
                        tool_context,
                    )
                    if init_result.get("status") == "success":
                        session_initialized.add(agent_name)
                        state['_mpst_initialized_agents'] = (
                            session_initialized
                        )
                    else:
                        return init_result
                except Exception as exc:
                    return {
                        'status': 'error',
                        'code': 'ProtocolSetupFailed',
                        'message': (
                            f'Failed to initialize protocol for '
                            f'{agent_name}: {exc}'
                        ),
                    }
            elif agent_name in session_initialized:
                logger.debug(
                    "[MPST] Skip auto-init: %s already initialized "
                    "in this session",
                    agent_name,
                )
            elif agent_name in self._protocol_initialized_agents:
                logger.debug(
                    "[MPST] Skip auto-init: %s already initialized globally",
                    agent_name,
                )

            # 发送前：校验真实对端，并将协议标签作为通信元数据封装到消息中。
            validation, protocol_message = (
                self.host_protocol_monitor.prepare_outgoing(
                    protocol_session_id,
                    peer=role,
                    content=message,
                )
            )
            if not validation['is_valid']:
                log_host_validation_error(
                    stage='host_send',
                    code=validation.get('code'),
                    error=validation.get('error'),
                    session_id=protocol_session_id,
                    peer=role,
                    position=validation.get('current_position'),
                    expected=validation.get('expected_transitions'),
                    content=protocol_message,
                    action='rejected_before_remote_send',
                )
                return {
                    'status': 'error',
                    'code': validation.get('code'),
                    'message': validation.get('error'),
                    'stage': 'host_send',
                }
        else:
            logger.info(
                "[VALIDATION DISABLED] Sending raw message to %s",
                agent_name,
            )

        request_message = Message(
            role=Role.user,
            parts=[Part(root=TextPart(text=protocol_message))],
            message_id=message_id,
            context_id=context_id,
            task_id=task_id,
        )
        log_a2a_communication(
            direction="outgoing",
            phase="business",
            peer=agent_name,
            context_id=context_id,
            task_id=task_id,
            message_id=message_id,
            payload=request_message,
        )
        response = await client.send_message(request_message)
        log_a2a_communication(
            direction="incoming",
            phase="business",
            peer=agent_name,
            context_id=context_id,
            task_id=task_id,
            message_id=message_id,
            payload=response,
        )

        if isinstance(response, Message):
            if self.validation_enabled:
                response_content = _extract_text_from_parts(response.parts)
                validation = self.host_protocol_monitor.validate_incoming(
                    protocol_session_id,
                    peer=role,
                    content=response_content,
                )
                if not validation['is_valid']:
                    log_host_validation_error(
                        stage='host_receive',
                        code=validation.get('code'),
                        error=validation.get('error'),
                        session_id=protocol_session_id,
                        peer=role,
                        position=validation.get('current_position'),
                        expected=validation.get('expected_transitions'),
                        content=response_content,
                        action='rejected_before_model_delivery',
                    )
                    return {
                        'status': 'error',
                        'code': validation.get('code'),
                        'message': validation.get('error'),
                        'stage': 'host_receive',
                    }
            return await convert_parts(response.parts, tool_context)
        task: Task = response
        # Assume completion unless a state returns that isn't complete
        state['session_active'] = task.status.state not in [
            TaskState.completed,
            TaskState.canceled,
            TaskState.failed,
            TaskState.unknown,
        ]
        if task.context_id:
            state['context_id'] = task.context_id
        state['task_id'] = task.id
        if task.status.state == TaskState.input_required:
            # Force user input back
            tool_context.actions.skip_summarization = True
            tool_context.actions.escalate = True
        elif task.status.state == TaskState.canceled:
            # Open question, should we return some info for cancellation instead
            raise ValueError(f'Agent {agent_name} task {task.id} is cancelled')
        elif task.status.state == TaskState.failed:
            # Raise error for failure
            raise ValueError(f'Agent {agent_name} task {task.id} failed')

        if self.validation_enabled:
            protocol_response = _extract_task_protocol_content(task)
            validation = self.host_protocol_monitor.validate_incoming(
                protocol_session_id,
                peer=role,
                content=protocol_response,
            )
            if not validation['is_valid']:
                log_host_validation_error(
                    stage='host_receive',
                    code=validation.get('code'),
                    error=validation.get('error'),
                    session_id=protocol_session_id,
                    peer=role,
                    position=validation.get('current_position'),
                    expected=validation.get('expected_transitions'),
                    content=protocol_response,
                    action='rejected_before_model_delivery',
                )
                return {
                    'status': 'error',
                    'code': validation.get('code'),
                    'message': validation.get('error'),
                    'stage': 'host_receive',
                }
            state['_mpst_protocol_complete'] = bool(
                validation.get('complete')
            )
        response = []
        if task.status.message:
            # Assume the information is in the task message.
            if ts := self.timestamp_extension.get_timestamp(
                task.status.message
            ):
                response.append(f'[at {ts.astimezone().isoformat()}]')
            response.extend(
                await convert_parts(task.status.message.parts, tool_context)
            )
        if task.artifacts:
            for artifact in task.artifacts:
                if ts := self.timestamp_extension.get_timestamp(artifact):
                    response.append(f'[at {ts.astimezone().isoformat()}]')
                response.extend(
                    await convert_parts(artifact.parts, tool_context)
                )
        logger.info(f"[SEND_MESSAGE] Completed for {agent_name}, response={str(response)[:100]}...")
        return response

    def finalize_protocol(self, tool_context: ToolContext):
        """Verify that the Host reached a legal protocol completion point."""
        state = tool_context.state
        if not self.validation_enabled:
            return {
                'status': 'success',
                'code': 'ValidationDisabled',
                'message': (
                    'Validation is disabled; no protocol completion '
                    'check was performed.'
                ),
                'current_position': None,
                'validation_enabled': False,
            }
        session_id = state.get('_mpst_session_id')
        if not session_id or not self.host_protocol_monitor.initialized:
            return {
                'status': 'error',
                'code': 'ProtocolNotInitialized',
                'message': 'No active MPST protocol session exists.',
            }
        result = self.host_protocol_monitor.finalize(session_id)
        state['_mpst_protocol_complete'] = result['is_valid']
        if not result['is_valid']:
            log_host_validation_error(
                stage='host_finalize',
                code=result.get('code'),
                error=result.get('error'),
                session_id=session_id,
                position=result.get('current_position'),
                expected=result.get('expected_transitions'),
                action='workflow_not_finalized',
            )
        return {
            'status': 'success' if result['is_valid'] else 'error',
            'code': result.get('code'),
            'message': 'Protocol completed.' if result['is_valid'] else result.get('error'),
            'current_position': result.get('current_position'),
        }


def _extract_text_from_parts(parts: list[Part] | None) -> str:
    if not parts:
        return ''
    for part in parts:
        root = getattr(part, 'root', part)
        text = getattr(root, 'text', None)
        if text is not None:
            return text
        data = getattr(root, 'data', None)
        if data is not None:
            return json.dumps(data, ensure_ascii=False)
    return ''


def _extract_task_protocol_content(task: Task) -> str:
    for artifact in task.artifacts or []:
        content = _extract_text_from_parts(artifact.parts)
        if content:
            return content
    if task.status.message:
        return _extract_text_from_parts(task.status.message.parts)
    return ''


async def convert_parts(parts: list[Part], tool_context: ToolContext):
    rval = []
    for p in parts:
        rval.append(await convert_part(p, tool_context))
    return rval


async def convert_part(part: Part, tool_context: ToolContext):
    if part.root.kind == 'text':
        return part.root.text
    if part.root.kind == 'data':
        return part.root.data
    if part.root.kind == 'file':
        # Repackage A2A FilePart to google.genai Blob
        # Currently not considering plain text as files
        file_id = part.root.file.name
        file_bytes = base64.b64decode(part.root.file.bytes)
        file_part = types.Part(
            inline_data=types.Blob(
                mime_type=part.root.file.mime_type, data=file_bytes
            )
        )
        await tool_context.save_artifact(file_id, file_part)
        tool_context.actions.skip_summarization = True
        tool_context.actions.escalate = True
        return DataPart(data={'artifact-file-id': file_id})
    return f'Unknown type: {part.kind}'
