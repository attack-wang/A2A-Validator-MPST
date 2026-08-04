"""A2A executor integration for the shared MPST runtime validator."""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any, Optional

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Message, Part, Role, Task, TaskState, TextPart, UnsupportedOperationError
from a2a.utils import new_agent_text_message, new_task
from a2a.utils.errors import ServerError

from .mpst_validator import MPSTValidator, ValidatorRegistry, ViolationCode
from .validation_config import resolve_validation_enabled

logger = logging.getLogger(__name__)


class MPSTValidationExtension:
    """Session-aware facade used by A2A executors."""

    def __init__(self, role_name: str = "Agent"):
        self.role_name = role_name
        self.registry = ValidatorRegistry(role_name)

    def set_protocol(self, local_protocol_text: str, protocol_id: str = "default") -> bool:
        return self.registry.register_protocol(protocol_id, local_protocol_text)

    def get_validator(self, session_id: str) -> MPSTValidator:
        return self.registry.get(session_id)

    def validate_incoming_message(
        self,
        message: Message,
        session_id: str,
        sender: str = "Host",
    ) -> dict[str, Any]:
        validator = self.get_validator(session_id)
        content = self._extract_message_content(message)
        return validator.validate_message(content, direction="receive", sender=sender)

    def validate_outgoing_content(
        self,
        content: Any,
        session_id: str,
        receiver: str = "Host",
        generation_metadata: Optional[dict[str, Any]] = None,
    ) -> tuple[dict[str, Any], str]:
        validator = self.get_validator(session_id)
        tool_check = validator.validate_tool_call_completion(
            content,
            generation_metadata,
        )
        if not tool_check["is_valid"]:
            return tool_check, self._content_text(content)
        wrapped = self.wrap_expected_label(content, validator, direction="send")
        result = validator.validate_message(
            wrapped,
            direction="send",
            receiver=receiver,
            check_tool_call=False,
        )
        return result, wrapped

    @staticmethod
    def wrap_expected_label(content: Any, validator: MPSTValidator, direction: str) -> str:
        text = content if isinstance(content, str) else json.dumps(content, ensure_ascii=False)
        expected = validator.expected_transition(direction)
        if not expected:
            return text
        actual = validator._extract_message_label(text)
        if actual.lower() == expected.label.lower() and (
            text.lstrip().startswith("[") or text.lstrip().lower().startswith(f"{expected.label.lower()}:")
        ):
            return text
        return f"[{expected.label}: {text}]"

    @staticmethod
    def _content_text(content: Any) -> str:
        if isinstance(content, str):
            return content
        try:
            return json.dumps(content, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            return str(content)

    @staticmethod
    def _extract_message_content(message: Message) -> Any:
        if not message or not message.parts:
            return ""
        for part in message.parts:
            root = getattr(part, "root", part)
            text = getattr(root, "text", None)
            if text is not None:
                return text
            data = getattr(root, "data", None)
            if data is not None:
                return data
        return ""

    def get_status(self, session_id: Optional[str] = None) -> dict[str, Any]:
        return self.registry.status(session_id)

    def reset(self, session_id: str) -> None:
        self.registry.reset_session(session_id)


class MPSTValidatingExecutor(AgentExecutor):
    """AgentExecutor that enforces a projected local protocol.

    A protocol setup message registers an immutable template. Each normal A2A
    context receives its own validator instance, preventing state leakage across
    users and tasks.
    """

    def __init__(
        self,
        role_name: str = "Agent",
        delegate: Any = None,
        *,
        max_tool_call_retries: int = 2,
        validation_enabled: Optional[bool] = None,
    ):
        self.role_name = role_name
        self.validation_enabled = resolve_validation_enabled(
            validation_enabled
        )
        self._validation_ext = MPSTValidationExtension(role_name)
        self._delegate = delegate
        self.agent = None
        self.max_tool_call_retries = max(0, int(max_tool_call_retries))
        logger.info(
            "[VALIDATION MODE] role=%s enabled=%s",
            role_name,
            self.validation_enabled,
        )

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.context_id)

        if self._is_protocol_setup_message(context.message):
            if not self.validation_enabled:
                await updater.update_status(
                    TaskState.completed,
                    message=updater.new_agent_message(
                        [
                            Part(
                                root=TextPart(
                                    text=(
                                        "Protocol setup skipped "
                                        "(validation disabled)"
                                    )
                                )
                            )
                        ]
                    ),
                    final=True,
                )
                return
            await self._handle_protocol_setup(context, updater)
            return

        if not self.validation_enabled:
            await self._execute_without_validation(context, task, updater)
            return

        await self._execute_with_validation(context, task, updater)

    async def _execute_without_validation(
        self,
        context: RequestContext,
        task: Task,
        updater: TaskUpdater,
    ) -> None:
        """Run the original A2A executor path without validation intervention."""
        query = self._validation_ext._extract_message_content(context.message)
        query_text = (
            query
            if isinstance(query, str)
            else json.dumps(query, ensure_ascii=False)
        )
        agent = (
            getattr(self._delegate, "agent", None)
            if self._delegate is not None
            else self.agent
        )
        if agent is None:
            agent = self.agent
        if agent is None:
            await self._fail(updater, "A2A executor has no delegate agent")
            return

        try:
            async for item in agent.stream(query_text, task.context_id):
                if not item.get("is_task_complete"):
                    await updater.update_status(
                        TaskState.working,
                        new_agent_text_message(
                            item.get("updates", "Processing..."),
                            task.context_id,
                            task.id,
                        ),
                    )
                    continue

                await updater.add_artifact(
                    [
                        Part(
                            root=TextPart(
                                text=str(item.get("content", ""))
                            )
                        )
                    ],
                    name="result",
                )
                logger.info(
                    "[VALIDATION DISABLED] role=%s raw output passed through",
                    self.role_name,
                )
                await updater.complete()
                return
        except Exception as exc:
            logger.exception("Unvalidated A2A execution failed")
            await self._fail(updater, f"Execution error: {exc}")

    async def _handle_protocol_setup(self, context: RequestContext, updater: TaskUpdater) -> None:
        protocol_data = self._extract_protocol_from_message(context.message)
        local_protocol = protocol_data.get("local_protocol", "") if protocol_data else ""
        protocol_id = protocol_data.get("protocol_name", "default") if protocol_data else "default"
        if not local_protocol:
            await self._fail(updater, "MPST protocol setup failed: no local protocol provided")
            return

        if not self._validation_ext.set_protocol(local_protocol, protocol_id):
            await self._fail(updater, "MPST protocol setup failed: invalid local protocol")
            return

        await updater.update_status(
            TaskState.completed,
            message=updater.new_agent_message(
                [Part(root=TextPart(text=f"MPST Protocol initialized successfully ({protocol_id})"))]
            ),
            final=True,
        )

    async def _execute_with_validation(
        self,
        context: RequestContext,
        task: Task,
        updater: TaskUpdater,
    ) -> None:
        session_id = self._session_id(context, task)
        if not self._validation_ext.registry.has_protocol():
            await self._fail(updater, "MPST protocol violation: protocol is not initialized")
            return

        try:
            incoming = self._validation_ext.validate_incoming_message(
                context.message,
                session_id,
                sender="Host",
            )
            if not incoming["is_valid"]:
                await self._fail(updater, self._violation_text("input", incoming))
                return

            await updater.update_status(TaskState.working)
            query = self._validation_ext._extract_message_content(context.message)
            query_text = query if isinstance(query, str) else json.dumps(query, ensure_ascii=False)
            agent = getattr(self._delegate, "agent", None) if self._delegate is not None else self.agent
            if agent is None:
                agent = self.agent
            if agent is None:
                await self._fail(updater, "MPST executor has no delegate agent")
                return

            generation_prompt = query_text
            tool_retry_count = 0
            while True:
                retry_requested = False
                final_response_seen = False

                async for item in agent.stream(generation_prompt, task.context_id):
                    if not item.get("is_task_complete"):
                        await updater.update_status(
                            TaskState.working,
                            new_agent_text_message(
                                item.get("updates", "Processing..."),
                                task.context_id,
                                task.id,
                            ),
                        )
                        continue

                    final_response_seen = True
                    content = item.get("content", "")
                    generation_metadata = dict(item)
                    generation_metadata.setdefault(
                        "tool_required",
                        bool(getattr(agent, "requires_tool_call", False)),
                    )
                    outgoing, wrapped_content = self._validation_ext.validate_outgoing_content(
                        content,
                        session_id,
                        receiver="Host",
                        generation_metadata=generation_metadata,
                    )
                    if not outgoing["is_valid"]:
                        if (
                            outgoing.get("code")
                            == ViolationCode.TOOL_CALL_INCOMPLETE.value
                            and outgoing.get("retryable")
                            and tool_retry_count < self.max_tool_call_retries
                        ):
                            tool_retry_count += 1
                            generation_prompt = self._tool_call_retry_prompt(
                                outgoing,
                                tool_retry_count,
                            )
                            await updater.update_status(
                                TaskState.working,
                                new_agent_text_message(
                                    (
                                        "The internal tool call was not completed; "
                                        f"regenerating ({tool_retry_count}/"
                                        f"{self.max_tool_call_retries})..."
                                    ),
                                    task.context_id,
                                    task.id,
                                ),
                            )
                            retry_requested = True
                            break
                        await self._fail(updater, self._violation_text("output", outgoing))
                        return

                    completed = self._validation_ext.get_validator(session_id).finalize()
                    if not completed["is_valid"]:
                        await self._fail(updater, self._violation_text("finalize", completed))
                        return

                    await updater.add_artifact(
                        [Part(root=TextPart(text=wrapped_content))],
                        name="result",
                    )
                    await updater.complete()
                    return

                if retry_requested:
                    continue
                if not final_response_seen:
                    await self._fail(updater, "Agent completed without a final protocol response")
                return
        except Exception as exc:
            logger.exception("MPST validated execution failed")
            await self._fail(updater, f"Execution error: {exc}")

    @staticmethod
    async def _fail(updater: TaskUpdater, text: str) -> None:
        await updater.update_status(
            TaskState.failed,
            message=updater.new_agent_message([Part(root=TextPart(text=text))]),
            final=True,
        )

    @staticmethod
    def _violation_text(stage: str, result: dict[str, Any]) -> str:
        code = result.get("code") or "ProtocolViolation"
        return f"MPST protocol violation during {stage}: {code}: {result.get('error')}"

    @staticmethod
    def _tool_call_retry_prompt(result: dict[str, Any], attempt: int) -> str:
        tool_name = result.get("tool_name")
        tool_hint = f" `{tool_name}`" if tool_name else ""
        return (
            "The previous response exposed an unexecuted, malformed, or incomplete "
            f"tool call{tool_hint}. Regenerate the tool call using the registered "
            "tool schema, wait for the tool response, and only then produce the final "
            f"business result. Do not print tool-call syntax as final text. "
            f"Recovery attempt: {attempt}."
        )

    @staticmethod
    def _session_id(context: RequestContext, task: Task) -> str:
        message = context.message
        return str(
            getattr(message, "context_id", None)
            or getattr(task, "context_id", None)
            or getattr(message, "task_id", None)
            or getattr(task, "id", None)
            or uuid.uuid4()
        )

    @staticmethod
    def _is_protocol_setup_message(message: Message) -> bool:
        data = MPSTValidatingExecutor._extract_json_message(message)
        return bool(data and data.get("type") == "protocol_setup")

    @staticmethod
    def _extract_protocol_from_message(message: Message) -> Optional[dict[str, Any]]:
        data = MPSTValidatingExecutor._extract_json_message(message)
        return data if data and data.get("type") == "protocol_setup" else None

    @staticmethod
    def _extract_json_message(message: Message) -> Optional[dict[str, Any]]:
        try:
            content = MPSTValidationExtension._extract_message_content(message)
            if isinstance(content, dict):
                return content
            parsed = json.loads(content)
            return parsed if isinstance(parsed, dict) else None
        except (json.JSONDecodeError, TypeError, ValueError):
            return None

    async def cancel(self, request: RequestContext, event_queue: EventQueue) -> None:
        raise ServerError(error=UnsupportedOperationError())

    def get_status(self, session_id: Optional[str] = None) -> dict[str, Any]:
        return {"protocol": self._validation_ext.get_status(session_id)}
