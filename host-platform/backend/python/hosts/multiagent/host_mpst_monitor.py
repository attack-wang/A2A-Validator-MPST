"""Session-aware Host-side MPST runtime monitor."""

from __future__ import annotations

from typing import Any, Optional

from mpst_ext import MPSTValidator, ValidatorRegistry


class HostProtocolMonitor:
    """Uses the same validator implementation as remote A2A agents."""

    def __init__(self):
        self.registry = ValidatorRegistry("Host")
        self.protocol_id = "default"

    @property
    def initialized(self) -> bool:
        return self.registry.has_protocol()

    def load_from_local_protocol(self, local_protocol_text: str, protocol_id: str = "default") -> bool:
        self.protocol_id = protocol_id
        return self.registry.register_protocol(protocol_id, local_protocol_text)

    def get_validator(self, session_id: str) -> MPSTValidator:
        return self.registry.get(session_id, self.protocol_id)

    def prepare_outgoing(
        self,
        session_id: str,
        *,
        peer: str,
        content: Any,
        label: Optional[str] = None,
    ) -> tuple[dict[str, Any], str]:
        validator = self.get_validator(session_id)
        # A protocol choice can expose several send transitions at once.
        # The selected remote peer disambiguates the branch and its label.
        expected = validator.expected_transition("send", peer=peer)
        selected_label = label or (expected.label if expected else None)
        wrapped = self._wrap(content, selected_label)
        result = validator.validate_message(
            wrapped,
            direction="send",
            receiver=peer,
            message_label=selected_label,
        )
        return result, wrapped

    def validate_incoming(
        self,
        session_id: str,
        *,
        peer: str,
        content: Any,
        label: Optional[str] = None,
    ) -> dict[str, Any]:
        validator = self.get_validator(session_id)
        return validator.validate_message(
            content,
            direction="receive",
            sender=peer,
            message_label=label,
        )

    def finalize(self, session_id: str) -> dict[str, Any]:
        return self.get_validator(session_id).finalize()

    def validate_final_output(
        self,
        session_id: str,
        content: Any,
    ) -> dict[str, Any]:
        """Reject tool-call syntax that leaked into Host user-facing output."""
        return self.get_validator(session_id).validate_tool_call_completion(
            content
        )

    def expected(self, session_id: str, direction: Optional[str] = None) -> Optional[dict[str, Any]]:
        transition = self.get_validator(session_id).expected_transition(direction)
        return transition.to_dict() if transition else None

    def reset(self, session_id: Optional[str] = None) -> None:
        if session_id:
            self.registry.reset_session(session_id)
        else:
            self.registry._sessions.clear()

    def get_status(self, session_id: Optional[str] = None) -> dict[str, Any]:
        return self.registry.status(session_id)

    @staticmethod
    def _wrap(content: Any, label: Optional[str]) -> str:
        text = str(content)
        if not label:
            return text
        stripped = text.lstrip()
        if stripped.startswith("[") or stripped.lower().startswith(f"{label.lower()}:"):
            return text
        return f"[{label}: {text}]"
