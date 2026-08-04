import asyncio
import base64
import concurrent.futures
import datetime
import json
import logging
import os
import uuid

import httpx

from a2a.types import (
    AgentCard,
    Artifact,
    DataPart,
    FilePart,
    FileWithBytes,
    FileWithUri,
    Message,
    Part,
    Role,
    Task,
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TextPart,
)
from google.adk import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.events.event import Event as ADKEvent
from google.adk.events.event_actions import EventActions as ADKEventActions
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from host_agent import HostAgent
from host_validation_logging import log_host_validation_error
from mpst_ext import MPSTValidator, resolve_validation_enabled
from remote_agent_connection import TaskCallbackArg
from utils.agent_card import get_agent_card

from service.server.application_manager import ApplicationManager
from service.types import Conversation, Event


logger = logging.getLogger(__name__)


class ADKHostManager(ApplicationManager):
    """An implementation of memory based management with fake agent actions

    This implements the interface of the ApplicationManager to plug into
    the AgentServer. This acts as the service contract that the Mesop app
    uses to send messages to the agent and provide information for the frontend.
    """

    _MAX_EMPTY_RESPONSE_RETRIES = 2
    _EMPTY_RESPONSE_RETRY_PROMPT = (
        'Your previous response contained no visible message content. Continue '
        'from the current session and protocol state. Do not repeat tool calls '
        'that already completed. Execute the next required tool if work remains. '
        'If the workflow is complete, call finalize_protocol and then provide a '
        'concise final answer containing the real tool results.'
    )
    _TOOL_CALL_LEAK_RETRY_PROMPT = (
        'Your previous response exposed a tool call as user-visible text instead '
        'of executing it. Continue from the current session and protocol state. '
        'Do not repeat tool calls that already completed. If another tool is '
        'required, emit a real structured function call and wait for its result. '
        'Never print Tool Calls JSON as the final answer. When the workflow is '
        'complete, call finalize_protocol and provide a normal user-facing answer.'
    )

    def __init__(
        self,
        http_client: httpx.AsyncClient,
        api_key: str = '',
        uses_vertex_ai: bool = False,
        validation_enabled: bool | None = None,
    ):
        self._conversations: list[Conversation] = []
        self._messages: list[Message] = []
        self._tasks: list[Task] = []
        self._events: dict[str, Event] = {}
        self._pending_message_ids: list[str] = []
        self._agents: list[AgentCard] = []
        self._artifact_chunks: dict[str, list[Artifact]] = {}
        self._session_service = InMemorySessionService()
        self._artifact_service = InMemoryArtifactService()
        self._memory_service = InMemoryMemoryService()
        self.validation_enabled = resolve_validation_enabled(
            validation_enabled
        )
        self._host_agent = HostAgent(
            [],
            http_client,
            self.task_callback,
            validation_enabled=self.validation_enabled,
        )
        self._context_to_conversation: dict[str, str] = {}
        self.user_id = 'test_user'
        self.app_name = 'A2A'
        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY', '')
        self.uses_vertex_ai = (
            uses_vertex_ai
            or os.environ.get('GOOGLE_GENAI_USE_VERTEXAI', '').upper() == 'TRUE'
        )
        logger.info(
            '[VALIDATION MODE] role=HostUI enabled=%s',
            self.validation_enabled,
        )

        # Set environment variables based on auth method
        if self.uses_vertex_ai:
            os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'TRUE'

        elif self.api_key:
            # Use API key authentication
            os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'FALSE'
            os.environ['GOOGLE_API_KEY'] = self.api_key

        self._initialize_host()

        # Map of message id to task id
        self._task_map: dict[str, str] = {}
        # Map to manage 'lost' message ids until protocol level id is introduced
        self._next_id: dict[
            str, str
        ] = {}  # dict[str, str]: previous message to next message

    def _initialize_host(self):
        agent = self._host_agent.create_agent()
        self._host_runner = Runner(
            app_name=self.app_name,
            agent=agent,
            artifact_service=self._artifact_service,
            session_service=self._session_service,
            memory_service=self._memory_service,
        )

    async def create_conversation(self) -> Conversation:
        session = await self._session_service.create_session(
            app_name=self.app_name, user_id=self.user_id
        )
        conversation_id = session.id
        c = Conversation(conversation_id=conversation_id, is_active=True)
        self._conversations.append(c)
        return c

    def update_api_key(self, api_key: str):
        """Update the API key and reinitialize the host if needed"""
        if api_key and api_key != self.api_key:
            self.api_key = api_key

            # Only update if not using Vertex AI
            if not self.uses_vertex_ai:
                os.environ['GOOGLE_API_KEY'] = api_key
                # Reinitialize host with new API key
                self._initialize_host()

                # Map of message id to task id
                self._task_map = {}

    def sanitize_message(self, message: Message) -> Message:
        if message.context_id:
            conversation = self.get_conversation(message.context_id)
            if not conversation:
                return message
            # Check if the last event in the conversation was tied to a task.
            if conversation.messages:
                task_id = conversation.messages[-1].task_id
                if task_id and task_still_open(
                    next(
                        filter(lambda x: x and x.id == task_id, self._tasks),
                        None,
                    )
                ):
                    message.task_id = task_id
        return message

    @staticmethod
    def _text_has_visible_content(text: str | None) -> bool:
        if not text or not text.strip():
            return False
        stripped = text.strip()
        lines = stripped.splitlines()
        if (
            len(lines) >= 2
            and lines[0].strip().startswith('```')
            and lines[-1].strip() == '```'
            and not ''.join(lines[1:-1]).strip()
        ):
            return False
        return True

    @classmethod
    def _message_has_visible_content(cls, message: Message | None) -> bool:
        if not message or not message.parts:
            return False
        for part in message.parts:
            root = part.root
            if root.kind == 'text':
                if cls._text_has_visible_content(root.text):
                    return True
            else:
                return True
        return False

    @staticmethod
    def _message_payload(message: Message | None) -> object:
        if not message:
            return ''
        payload: list[object] = []
        for part in message.parts:
            root = part.root
            if root.kind == 'text':
                payload.append(root.text)
            elif root.kind == 'data':
                payload.append(root.data)
        if len(payload) == 1:
            return payload[0]
        return payload

    @classmethod
    def _message_contains_tool_call_payload(
        cls,
        message: Message | None,
    ) -> bool:
        return MPSTValidator.contains_tool_call_payload(
            cls._message_payload(message)
        )

    @classmethod
    def _empty_response_retry_content(cls) -> types.Content:
        return types.Content(
            role='user',
            parts=[types.Part.from_text(text=cls._EMPTY_RESPONSE_RETRY_PROMPT)],
        )

    @classmethod
    def _tool_call_leak_retry_content(cls) -> types.Content:
        return types.Content(
            role='user',
            parts=[
                types.Part.from_text(
                    text=cls._TOOL_CALL_LEAK_RETRY_PROMPT
                )
            ],
        )

    async def _record_host_tool_call_violation(
        self,
        message: Message | None,
        context_id: str | None,
    ) -> dict[str, object] | None:
        """Record Host tool-call leakage in the active protocol validator."""
        if not context_id:
            return None
        session = await self._session_service.get_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=context_id,
        )
        state = getattr(session, 'state', {}) if session else {}
        protocol_session_id = state.get('_mpst_session_id')
        host_agent = getattr(self, '_host_agent', None)
        monitor = getattr(host_agent, 'host_protocol_monitor', None)
        if protocol_session_id and monitor and monitor.initialized:
            return monitor.validate_final_output(
                protocol_session_id,
                self._message_payload(message),
            )
        return None

    @staticmethod
    def _error_response(
        text: str,
        context_id: str | None,
        task_id: str | None,
    ) -> Message:
        return Message(
            role=Role.agent,
            parts=[Part(root=TextPart(text=text))],
            context_id=context_id,
            task_id=task_id,
            message_id=str(uuid.uuid4()),
        )

    async def process_message(self, message: Message) -> None:
        message_id = message.message_id
        if message_id:
            self._pending_message_ids.append(message_id)
        context_id = message.context_id
        conversation = self.get_conversation(context_id)
        response: Message | None = None
        task_id = message.task_id

        try:
            self._messages.append(message)
            if conversation:
                conversation.messages.append(message)
            self.add_event(
                Event(
                    id=str(uuid.uuid4()),
                    actor='user',
                    content=message,
                    timestamp=datetime.datetime.now(datetime.UTC).timestamp(),
                )
            )

            # Determine if a task is to be resumed.
            session = await self._session_service.get_session(
                app_name=self.app_name,
                user_id=self.user_id,
                session_id=context_id,
            )
            state_update = {
                'task_id': task_id,
                'context_id': context_id,
                'message_id': message.message_id,
            }
            # Need to upsert session state now, only way is to append an event.
            await self._session_service.append_event(
                session,
                ADKEvent(
                    id=ADKEvent.new_id(),
                    author='host_agent',
                    invocation_id=ADKEvent.new_id(),
                    actions=ADKEventActions(state_delta=state_update),
                ),
            )

            next_message = self.adk_content_from_message(message)
            for attempt in range(self._MAX_EMPTY_RESPONSE_RETRIES + 1):
                final_candidate: Message | None = None

                async for event in self._host_runner.run_async(
                    user_id=self.user_id,
                    session_id=context_id,
                    new_message=next_message,
                ):
                    if (
                        event.actions.state_delta
                        and 'task_id' in event.actions.state_delta
                    ):
                        task_id = event.actions.state_delta['task_id']

                    converted = (
                        await self.adk_content_to_message(
                            event.content, context_id, task_id
                        )
                        if event.content
                        else None
                    )
                    # Empty ADK events are state/control events. Keep them in the
                    # ADK session, but do not expose them as blank chat messages.
                    if converted and converted.parts:
                        self.add_event(
                            Event(
                                id=event.id,
                                actor=event.author,
                                content=converted,
                                timestamp=event.timestamp,
                            )
                        )
                    if event.is_final_response():
                        final_candidate = converted

                if not getattr(self, 'validation_enabled', True):
                    # Baseline mode preserves the model's raw final response.
                    # It does not detect, reject, or retry empty/tool-call output.
                    logger.info(
                        "[VALIDATION DISABLED] Preserving raw Host final "
                        "output for message %s: %r",
                        message_id,
                        self._message_payload(final_candidate),
                    )
                    response = final_candidate
                    break

                if self._message_has_visible_content(final_candidate):
                    if self._message_contains_tool_call_payload(
                        final_candidate
                    ):
                        tool_violation = (
                            await self._record_host_tool_call_violation(
                                final_candidate,
                                context_id,
                            )
                        )
                        log_host_validation_error(
                            stage='host_final_output',
                            code=(
                                tool_violation.get('code')
                                if tool_violation
                                else 'ToolCallIncomplete'
                            ),
                            error=(
                                tool_violation.get('error')
                                if tool_violation
                                else (
                                    'Tool-call syntax leaked into the final '
                                    'Host output'
                                )
                            ),
                            session_id=context_id,
                            position=(
                                tool_violation.get('current_position')
                                if tool_violation
                                else None
                            ),
                            expected=(
                                tool_violation.get('expected_transitions')
                                if tool_violation
                                else None
                            ),
                            content=self._message_payload(final_candidate),
                            action=(
                                'rejected_and_retrying'
                                if attempt
                                < self._MAX_EMPTY_RESPONSE_RETRIES
                                else 'rejected_after_retry_limit'
                            ),
                        )
                        if attempt < self._MAX_EMPTY_RESPONSE_RETRIES:
                            logger.warning(
                                'Host model exposed a tool call in user-facing '
                                'content for message %s; retrying (%s/%s)',
                                message_id,
                                attempt + 1,
                                self._MAX_EMPTY_RESPONSE_RETRIES,
                            )
                            next_message = (
                                self._tool_call_leak_retry_content()
                            )
                            continue
                        response = self._error_response(
                            'Host 模型连续将工具调用作为普通文本输出，系统已拒绝'
                            '向用户展示该内容。请重新发送请求。',
                            context_id,
                            task_id,
                        )
                        break
                    response = final_candidate
                    break

                if attempt < self._MAX_EMPTY_RESPONSE_RETRIES:
                    log_host_validation_error(
                        stage='host_model_output',
                        code='EmptyModelResponse',
                        error='Host model returned no visible message content',
                        session_id=context_id,
                        action='retrying_same_session',
                    )
                    logger.warning(
                        'Host model returned no visible content for message %s; '
                        'continuing from the current session (retry %s/%s)',
                        message_id,
                        attempt + 1,
                        self._MAX_EMPTY_RESPONSE_RETRIES,
                    )
                    next_message = self._empty_response_retry_content()
                    continue

                log_host_validation_error(
                    stage='host_model_output',
                    code='EmptyModelResponse',
                    error=(
                        'Host model returned no visible message content after '
                        f'{self._MAX_EMPTY_RESPONSE_RETRIES} retries'
                    ),
                    session_id=context_id,
                    action='visible_error_returned',
                )
                response = self._error_response(
                    'Host 模型连续返回空内容，系统已自动重试 '
                    f'{self._MAX_EMPTY_RESPONSE_RETRIES} 次，但仍未生成可显示的'
                    '最终回答。远程工具可能已经执行，请查看事件记录后重新发送请求。',
                    context_id,
                    task_id,
                )

        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.exception(
                'Failed to process message %s in conversation %s',
                message_id,
                context_id,
            )
            log_host_validation_error(
                stage='host_processing',
                code=type(exc).__name__,
                error=str(exc),
                session_id=context_id,
                action='visible_error_returned',
            )
            response = self._error_response(
                f'处理请求时发生错误：{type(exc).__name__}: {exc}',
                context_id,
                task_id,
            )
        finally:
            if response:
                self._messages.append(response)
                if conversation:
                    conversation.messages.append(response)
                if not any(
                    event.content.message_id == response.message_id
                    for event in self._events.values()
                ):
                    self.add_event(
                        Event(
                            id=str(uuid.uuid4()),
                            actor='host_agent',
                            content=response,
                            timestamp=datetime.datetime.now(
                                datetime.UTC
                            ).timestamp(),
                        )
                    )
            if message_id and message_id in self._pending_message_ids:
                self._pending_message_ids.remove(message_id)

    def add_task(self, task: Task):
        self._tasks.append(task)

    def update_task(self, task: Task):
        for i, t in enumerate(self._tasks):
            if t.id == task.id:
                self._tasks[i] = task
                return

    def task_callback(self, task: TaskCallbackArg, agent_card: AgentCard):
        self.emit_event(task, agent_card)
        if isinstance(task, TaskStatusUpdateEvent):
            current_task = self.add_or_get_task(task)
            current_task.status = task.status
            self.attach_message_to_task(task.status.message, current_task.id)
            self.insert_message_history(current_task, task.status.message)
            self.update_task(current_task)
            return current_task
        if isinstance(task, TaskArtifactUpdateEvent):
            current_task = self.add_or_get_task(task)
            self.process_artifact_event(current_task, task)
            self.update_task(current_task)
            return current_task
        # Otherwise this is a Task, either new or updated
        if not any(filter(lambda x: x and x.id == task.id, self._tasks)):
            self.attach_message_to_task(task.status.message, task.id)
            self.add_task(task)
            return task
        self.attach_message_to_task(task.status.message, task.id)
        self.update_task(task)
        return task

    def emit_event(self, task: TaskCallbackArg, agent_card: AgentCard):
        content = None
        context_id = task.context_id
        if isinstance(task, TaskStatusUpdateEvent):
            if task.status.message:
                content = task.status.message
            else:
                content = Message(
                    parts=[Part(root=TextPart(text=str(task.status.state)))],
                    role=Role.agent,
                    message_id=str(uuid.uuid4()),
                    context_id=context_id,
                    task_id=task.task_id,
                )
        elif isinstance(task, TaskArtifactUpdateEvent):
            content = Message(
                parts=task.artifact.parts,
                role=Role.agent,
                message_id=str(uuid.uuid4()),
                context_id=context_id,
                task_id=task.task_id,
            )
        elif task.status and task.status.message:
            content = task.status.message
        elif task.artifacts:
            parts = []
            for a in task.artifacts:
                parts.extend(a.parts)
            content = Message(
                parts=parts,
                role=Role.agent,
                message_id=str(uuid.uuid4()),
                task_id=task.id,
                context_id=context_id,
            )
        else:
            content = Message(
                parts=[Part(root=TextPart(text=str(task.status.state)))],
                role=Role.agent,
                message_id=str(uuid.uuid4()),
                task_id=task.id,
                context_id=context_id,
            )
        if content:
            self.add_event(
                Event(
                    id=str(uuid.uuid4()),
                    actor=agent_card.name,
                    content=content,
                    timestamp=datetime.datetime.utcnow().timestamp(),
                )
            )

    def attach_message_to_task(self, message: Message | None, task_id: str):
        if message:
            self._task_map[message.message_id] = task_id

    def insert_message_history(self, task: Task, message: Message | None):
        if not message:
            return
        if task.history is None:
            task.history = []
        message_id = message.message_id
        if not message_id:
            return
        if task.history and (
            task.status.message
            and task.status.message.message_id
            not in [x.message_id for x in task.history]
        ):
            task.history.append(task.status.message)
        elif not task.history and task.status.message:
            task.history = [task.status.message]
        else:
            print(
                'Message id already in history',
                task.status.message.message_id if task.status.message else '',
                task.history,
            )

    def add_or_get_task(self, event: TaskCallbackArg):
        task_id = None
        if isinstance(event, Message):
            task_id = event.task_id
        elif isinstance(event, Task):
            task_id = event.id
        else:
            task_id = event.task_id
        if not task_id:
            task_id = str(uuid.uuid4())
        current_task = next(
            filter(lambda x: x.id == task_id, self._tasks), None
        )
        if not current_task:
            context_id = event.context_id
            current_task = Task(
                id=task_id,
                # initialize with submitted
                status=TaskStatus(state=TaskState.submitted),
                artifacts=[],
                context_id=context_id,
            )
            self.add_task(current_task)
            return current_task

        return current_task

    def process_artifact_event(
        self, current_task: Task, task_update_event: TaskArtifactUpdateEvent
    ):
        artifact = task_update_event.artifact
        if not task_update_event.append:
            # received the first chunk or entire payload for an artifact
            if (
                task_update_event.last_chunk is None
                or task_update_event.last_chunk
            ):
                # last_chunk bit is missing or is set to true, so this is the entire payload
                # add this to artifacts
                if not current_task.artifacts:
                    current_task.artifacts = []
                current_task.artifacts.append(artifact)
            else:
                # this is a chunk of an artifact, stash it in temp store for assembling
                if artifact.artifact_id not in self._artifact_chunks:
                    self._artifact_chunks[artifact.artifact_id] = []
                self._artifact_chunks[artifact.artifact_id].append(artifact)
        else:
            # we received an append chunk, add to the existing temp artifact
            current_temp_artifact = self._artifact_chunks[artifact.artifact_id][
                -1
            ]
            # TODO handle if current_temp_artifact is missing
            current_temp_artifact.parts.extend(artifact.parts)
            if task_update_event.last_chunk:
                if current_task.artifacts:
                    current_task.artifacts.append(current_temp_artifact)
                else:
                    current_task.artifacts = [current_temp_artifact]
                del self._artifact_chunks[artifact.artifact_id][-1]

    def add_event(self, event: Event):
        self._events[event.id] = event

    def get_conversation(
        self, conversation_id: str | None
    ) -> Conversation | None:
        if not conversation_id:
            return None
        return next(
            filter(
                lambda c: c and c.conversation_id == conversation_id,
                self._conversations,
            ),
            None,
        )

    def get_pending_messages(self) -> list[tuple[str, str]]:
        rval = []
        for message_id in self._pending_message_ids:
            if message_id in self._task_map:
                task_id = self._task_map[message_id]
                task = next(
                    filter(lambda x: x.id == task_id, self._tasks), None
                )
                if not task:
                    rval.append((message_id, ''))
                elif task.history and task.history[-1].parts:
                    if len(task.history) == 1:
                        rval.append((message_id, 'Working...'))
                    else:
                        part = task.history[-1].parts[0]
                        rval.append(
                            (
                                message_id,
                                part.root.text
                                if part.root.kind == 'text'
                                else 'Working...',
                            )
                        )
            else:
                rval.append((message_id, ''))
        return rval

    def register_agent(self, url):
        agent_data = get_agent_card(url)
        if not agent_data.url:
            agent_data.url = url
        self._agents.append(agent_data)
        self._host_agent.register_agent_card(agent_data)
        # Now update the host agent definition
        self._initialize_host()

    @property
    def agents(self) -> list[AgentCard]:
        return self._agents

    @property
    def conversations(self) -> list[Conversation]:
        return self._conversations

    @property
    def tasks(self) -> list[Task]:
        return self._tasks

    @property
    def events(self) -> list[Event]:
        return sorted(self._events.values(), key=lambda x: x.timestamp)

    def adk_content_from_message(self, message: Message) -> types.Content:
        parts: list[types.Part] = []
        for p in message.parts:
            part = p.root
            if part.kind == 'text':
                parts.append(types.Part.from_text(text=part.text))
            elif part.kind == 'data':
                json_string = json.dumps(part.data)
                parts.append(types.Part.from_text(text=json_string))
            elif part.kind == 'file':
                if isinstance(part.file, FileWithUri):
                    parts.append(
                        types.Part.from_uri(
                            file_uri=part.file.uri,
                            mime_type=part.file.mime_type,
                        )
                    )
                else:
                    parts.append(
                        types.Part.from_bytes(
                            data=part.file.bytes.encode('utf-8'),
                            mime_type=part.file.mime_type,
                        )
                    )
        return types.Content(parts=parts, role=message.role)

    async def adk_content_to_message(
        self,
        content: types.Content,
        context_id: str | None,
        task_id: str | None,
    ) -> Message:
        parts: list[Part] = []
        if not content.parts:
            return Message(
                parts=[],
                role=content.role if content.role == Role.user else Role.agent,
                context_id=context_id,
                task_id=task_id,
                message_id=str(uuid.uuid4()),
            )
        for part in content.parts:
            if part.text:
                # try parse as data
                try:
                    data = json.loads(part.text)
                    parts.append(Part(root=DataPart(data=data)))
                except:  # noqa: E722
                    parts.append(Part(root=TextPart(text=part.text)))
            elif part.inline_data:
                parts.append(
                    Part(
                        root=FilePart(
                            file=FileWithBytes(
                                bytes=part.inline_data.decode('utf-8'),
                                mime_type=part.file_data.mime_type,
                            ),
                        )
                    )
                )
            elif part.file_data:
                parts.append(
                    Part(
                        root=FilePart(
                            file=FileWithUri(
                                uri=part.file_data.file_uri,
                                mime_type=part.file_data.mime_type,
                            )
                        )
                    )
                )
            # These aren't managed by the A2A message structure, these are internal
            # details of ADK, we will simply flatten these to json representations.
            elif part.video_metadata:
                parts.append(
                    Part(root=DataPart(data=part.video_metadata.model_dump()))
                )
            elif part.thought:
                parts.append(Part(root=TextPart(text='thought')))
            elif part.executable_code:
                parts.append(
                    Part(root=DataPart(data=part.executable_code.model_dump()))
                )
            elif part.function_call:
                parts.append(
                    Part(root=DataPart(data=part.function_call.model_dump()))
                )
            elif part.function_response:
                parts.extend(
                    await self._handle_function_response(
                        part, context_id, task_id
                    )
                )
            else:
                raise ValueError('Unexpected content, unknown type')
        return Message(
            role=content.role if content.role == Role.user else Role.agent,
            parts=parts,
            context_id=context_id,
            task_id=task_id,
            message_id=str(uuid.uuid4()),
        )

    def _normalize_tool_response_payload(self, raw_resp: object) -> list[object]:
        """ADK / LiteLLM may return function_response.response as dict with
        'result', as a plain dict/list, or as a pydantic model. Normalize to a list
        of renderable items.
        """
        if raw_resp is None:
            return []
        if hasattr(raw_resp, 'model_dump'):
            raw_resp = raw_resp.model_dump()
        if isinstance(raw_resp, dict):
            if 'result' in raw_resp:
                payload = raw_resp['result']
            else:
                payload = raw_resp
        else:
            payload = raw_resp
        if payload is None:
            return []
        if isinstance(payload, (list, tuple)):
            return list(payload)
        return [payload]

    async def _handle_function_response(
        self, part: types.Part, context_id: str | None, task_id: str | None
    ) -> list[Part]:
        parts: list[Part] = []
        try:
            fr = part.function_response
            if fr is None:
                return [Part(root=TextPart(text='（空工具响应）'))]

            raw_resp = fr.response
            items = self._normalize_tool_response_payload(raw_resp)
            if not items:
                return [
                    Part(
                        root=TextPart(
                            text=json.dumps(
                                raw_resp,
                                ensure_ascii=False,
                                indent=2,
                                default=str,
                            )
                            if raw_resp is not None
                            else '（工具无返回内容）'
                        )
                    )
                ]

            for p in items:
                if isinstance(p, str):
                    parts.append(Part(root=TextPart(text=p)))
                elif isinstance(p, dict):
                    if 'kind' in p and p['kind'] == 'file':
                        parts.append(Part(root=FilePart(**p)))
                    else:
                        # DataPart 在聊天 UI 里常常不显示正文；工具 dict 用 JSON 文本展示
                        parts.append(
                            Part(
                                root=TextPart(
                                    text=json.dumps(
                                        p, ensure_ascii=False, indent=2
                                    )
                                )
                            )
                        )
                elif isinstance(p, DataPart):
                    if 'artifact-file-id' in p.data:
                        file_part = await self._artifact_service.load_artifact(
                            user_id=self.user_id,
                            session_id=context_id,
                            app_name=self.app_name,
                            filename=p.data['artifact-file-id'],
                        )
                        file_data = file_part.inline_data
                        base64_data = base64.b64encode(file_data.data).decode(
                            'utf-8'
                        )
                        parts.append(
                            Part(
                                root=FilePart(
                                    file=FileWithBytes(
                                        bytes=base64_data,
                                        mime_type=file_data.mime_type,
                                        name='artifact_file',
                                    )
                                )
                            )
                        )
                    else:
                        parts.append(
                            Part(
                                root=TextPart(
                                    text=json.dumps(
                                        p.data,
                                        ensure_ascii=False,
                                        indent=2,
                                    )
                                )
                            )
                        )
                else:
                    parts.append(
                        Part(root=TextPart(text=str(p)))
                    )
        except Exception as e:
            print("Couldn't convert to messages:", e)
            try:
                dump = part.function_response.model_dump()
            except Exception:
                dump = {'error': str(e)}
            parts.append(
                Part(
                    root=TextPart(
                        text=json.dumps(dump, ensure_ascii=False, indent=2)
                    )
                )
            )
        return parts

    def process_message_threadsafe(
        self, message: Message, loop: asyncio.AbstractEventLoop
    ) -> concurrent.futures.Future[None]:
        """Safely run process_message from a thread using the given event loop."""
        future = asyncio.run_coroutine_threadsafe(
            self.process_message(message), loop
        )
        future.add_done_callback(self._log_processing_future_result)
        return future

    @staticmethod
    def _log_processing_future_result(
        future: concurrent.futures.Future[None],
    ) -> None:
        try:
            future.result()
        except concurrent.futures.CancelledError:
            logger.warning('Message processing future was cancelled')
        except Exception as exc:
            logger.error(
                'Unhandled exception in message processing future',
                exc_info=(type(exc), exc, exc.__traceback__),
            )


def get_message_id(m: Message | None) -> str | None:
    if not m or not m.metadata or 'message_id' not in m.metadata:
        return None
    return m.metadata['message_id']


def task_still_open(task: Task | None) -> bool:
    if not task:
        return False
    return task.status.state in [
        TaskState.submitted,
        TaskState.working,
        TaskState.input_required,
    ]
