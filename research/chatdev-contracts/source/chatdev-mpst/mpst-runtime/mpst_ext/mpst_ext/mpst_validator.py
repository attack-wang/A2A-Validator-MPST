"""Shared MPST protocol parser and runtime validator.

The validator compiles projected local types into a small protocol automaton.
It supports sequencing, choices, recursion and finite termination. Runtime state
is deliberately kept separate from the protocol text so callers can create one
validator per A2A context/session.
"""

from __future__ import annotations

import copy
import json
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional

logger = logging.getLogger(__name__)


class MessageType(Enum):
    SEND = "send"
    RECEIVE = "receive"


class ViolationCode(Enum):
    WRONG_DIRECTION = "WrongDirection"
    WRONG_PEER = "WrongPeer"
    WRONG_LABEL = "WrongLabel"
    WRONG_TYPE = "WrongType"
    WRONG_ORDER = "WrongOrder"
    TOOL_CALL_INCOMPLETE = "ToolCallIncomplete"
    INCOMPLETE_PROTOCOL = "IncompleteProtocol"
    PROTOCOL_NOT_INITIALIZED = "ProtocolNotInitialized"


def _is_int(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    try:
        int(str(value).strip())
        return True
    except (ValueError, TypeError):
        return False


def _is_float(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    try:
        float(str(value).strip())
        return True
    except (ValueError, TypeError):
        return False


def _is_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return True
    return str(value).strip().lower() in {"true", "false", "1", "0"}


def _is_json(value: Any) -> bool:
    if isinstance(value, (dict, list)):
        return True
    try:
        json.loads(str(value))
        return True
    except (json.JSONDecodeError, TypeError, ValueError):
        return False


TYPE_VALIDATORS = {
    "int": _is_int,
    "float": _is_float,
    "number": lambda value: _is_int(value) or _is_float(value),
    "str": lambda value: isinstance(value, str),
    "string": lambda value: isinstance(value, str),
    "bool": _is_bool,
    "json": _is_json,
}


def validate_value_type(value: Any, expected_type: Optional[str]) -> tuple[bool, Optional[str]]:
    if not expected_type:
        return True, None
    validator = TYPE_VALIDATORS.get(expected_type.lower())
    if validator is None:
        return False, f"Unsupported protocol data type '{expected_type}'"
    if validator(value):
        return True, None
    return False, f"Type error: value {value!r} is not a valid {expected_type}"


@dataclass
class ProtocolTransition:
    action: MessageType
    peer: str
    label: str
    data_type: Optional[str]
    target: str

    @property
    def sender(self) -> Optional[str]:
        return self.peer if self.action == MessageType.RECEIVE else None

    @property
    def receiver(self) -> Optional[str]:
        return self.peer if self.action == MessageType.SEND else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action.value,
            "peer": self.peer,
            "label": self.label,
            "data_type": self.data_type,
            "target": self.target,
        }


@dataclass
class ProtocolState:
    name: str
    transitions: list[ProtocolTransition] = field(default_factory=list)
    is_terminal: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "is_terminal": self.is_terminal,
            "transitions": [transition.to_dict() for transition in self.transitions],
        }


# Backward-compatible name used by earlier code and documentation.
ProtocolPosition = ProtocolState


@dataclass
class _Interaction:
    peer: str
    action: str
    label: str


@dataclass
class _Sequence:
    items: list[Any]


@dataclass
class _Choice:
    alternatives: list[Any]


@dataclass
class _Recursion:
    variable: str
    body: Any


@dataclass
class _Variable:
    name: str


class _End:
    pass


class _Empty:
    pass


class _LocalTypeParser:
    """Small recursive-descent parser for the projection tool's text format."""

    TOKEN_RE = re.compile(r"(?:[A-Za-z_]\w*(?:__\w+)?)|(?:[\w]+)|[μ��]|[!?+().]", re.UNICODE)

    def __init__(self, text: str):
        # Projection files sometimes include a human-readable heading.
        if "projection for" in text.lower() and ":" in text:
            text = text.split(":", 1)[1]
        self.tokens = self.TOKEN_RE.findall(text)
        self.index = 0

    def parse(self) -> Any:
        node = self._parse_expression(stop=set())
        return node

    def _peek(self) -> Optional[str]:
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def _take(self) -> Optional[str]:
        token = self._peek()
        if token is not None:
            self.index += 1
        return token

    def _parse_expression(self, stop: set[str]) -> Any:
        alternatives = [self._parse_sequence(stop | {"+"})]
        while self._peek() == "+":
            self._take()
            alternatives.append(self._parse_sequence(stop | {"+"}))
        if len(alternatives) == 1:
            return alternatives[0]
        return _Choice(alternatives)

    def _parse_sequence(self, stop: set[str]) -> Any:
        items: list[Any] = []
        while (token := self._peek()) is not None and token not in stop:
            if token == ".":
                self._take()
                continue
            if token in {"μ", "��"} or token.lower() == "mu":
                self._take()
                variable = self._take()
                if not variable:
                    raise ValueError("Missing recursion variable after μ")
                if self._peek() == ".":
                    self._take()
                body = self._parse_expression(stop)
                items.append(_Recursion(variable, body))
                break
            if token == "(":
                self._take()
                items.append(self._parse_expression({")"}))
                if self._peek() != ")":
                    raise ValueError("Unclosed local protocol group")
                self._take()
                continue
            if token == "0" or token.lower() == "end":
                self._take()
                items.append(_End())
                continue

            name = self._take()
            action = self._peek()
            if action in {"!", "?"}:
                self._take()
                label = self._take()
                if not label:
                    raise ValueError(f"Missing message label after {name}{action}")
                items.append(_Interaction(name, action, label))
            else:
                items.append(_Variable(name))

        if not items:
            return _Empty()
        if len(items) == 1:
            return items[0]
        return _Sequence(items)


class LocalProtocol:
    """Compiled local protocol automaton with mutable per-session state."""

    def __init__(self, protocol_text: str, role_name: str):
        self.protocol_text = protocol_text
        self.role_name = role_name
        self.states: dict[str, ProtocolState] = {}
        self.position_history: list[str] = []
        self._counter = 0
        if "Initial State:" in protocol_text and "Transitions:" in protocol_text:
            self.recursive = False
            self._load_projected_fsm(protocol_text)
            self.positions = self.states
            self.rec_entry_position = None
            return
        self.recursive = bool(
            re.search(r"(?:[μ��]|\bmu)\s*\w+\s*\.", protocol_text, re.IGNORECASE)
        )
        ast = _LocalTypeParser(protocol_text).parse()
        terminal = self._new_state(is_terminal=True)
        entry = self._compile(ast, terminal, {})
        self.initial_position = entry
        self.current_position = entry
        self.rec_entry_position = entry if self.recursive else None
        self.positions = self.states  # compatibility alias
        if not self.states[entry].transitions and not self.states[entry].is_terminal:
            raise ValueError("Local protocol contains no executable transitions")

    def _load_projected_fsm(self, protocol_text: str) -> None:
        """Load the textual FSM emitted by subset projection."""
        initial_match = re.search(r"^Initial State:\s*(.+?)\s*$", protocol_text, re.MULTILINE)
        if not initial_match:
            raise ValueError("Subset projection has no initial state")

        state_names: dict[str, str] = {}

        def local_name(raw: str) -> str:
            normalized = raw.strip()
            if normalized not in state_names:
                state_names[normalized] = self._new_state()
            return state_names[normalized]

        raw_initial = initial_match.group(1).strip()
        local_name(raw_initial)
        current_source: Optional[str] = None

        for raw_line in protocol_text.splitlines():
            line = raw_line.rstrip()
            stripped = line.strip()
            if not stripped or stripped in {"Transitions:"} or stripped.startswith("Initial State:"):
                continue
            if not line[:1].isspace() and stripped.endswith(":"):
                current_source = stripped[:-1].strip()
                local_name(current_source)
                continue
            transition_match = re.match(r"^\s*\(([^,]+),\s*(.+)\)\s*$", line)
            if not transition_match or current_source is None:
                continue
            action_text = transition_match.group(1).strip()
            raw_target = transition_match.group(2).strip()
            action_match = re.match(r"^(\w+)\s*([!?])\s*(\w+(?:__\w+)?)$", action_text)
            if not action_match:
                raise ValueError(f"Unsupported subset transition: {action_text!r}")
            peer, direction, raw_label = action_match.groups()
            label, data_type = self._split_label_type(raw_label)
            self.states[local_name(current_source)].transitions.append(
                ProtocolTransition(
                    action=MessageType.SEND if direction == "!" else MessageType.RECEIVE,
                    peer=peer,
                    label=label.lower(),
                    data_type=data_type,
                    target=local_name(raw_target),
                )
            )

        self.initial_position = local_name(raw_initial)
        self.current_position = self.initial_position
        for state in self.states.values():
            state.is_terminal = not state.transitions
        if self.states[self.initial_position].is_terminal:
            raise ValueError("Subset projection initial state has no transitions")

    def _new_state(self, *, is_terminal: bool = False) -> str:
        name = f"pos_{self._counter}"
        self._counter += 1
        self.states[name] = ProtocolState(name=name, is_terminal=is_terminal)
        return name

    def _compile(self, node: Any, continuation: str, env: dict[str, str]) -> str:
        if isinstance(node, _Empty):
            return continuation
        if isinstance(node, _End):
            return continuation
        if isinstance(node, _Variable):
            if node.name not in env:
                # Projection strings may contain decorative identifiers. Fail closed.
                raise ValueError(f"Unknown recursion variable '{node.name}'")
            return env[node.name]
        if isinstance(node, _Interaction):
            state = self._new_state()
            label, data_type = self._split_label_type(node.label)
            self.states[state].transitions.append(
                ProtocolTransition(
                    action=MessageType.SEND if node.action == "!" else MessageType.RECEIVE,
                    peer=node.peer,
                    label=label.lower(),
                    data_type=data_type,
                    target=continuation,
                )
            )
            return state
        if isinstance(node, _Sequence):
            current = continuation
            for item in reversed(node.items):
                current = self._compile(item, current, env)
            return current
        if isinstance(node, _Choice):
            choice_state = self._new_state()
            for alternative in node.alternatives:
                entry = self._compile(alternative, continuation, env)
                entry_state = self.states[entry]
                if entry_state.is_terminal:
                    self.states[choice_state].is_terminal = True
                self.states[choice_state].transitions.extend(copy.deepcopy(entry_state.transitions))
            if not self.states[choice_state].transitions and not self.states[choice_state].is_terminal:
                raise ValueError("Choice contains no executable alternatives")
            return choice_state
        if isinstance(node, _Recursion):
            entry = self._new_state()
            nested_env = dict(env)
            nested_env[node.variable] = entry
            body_entry = self._compile(node.body, continuation, nested_env)
            if body_entry != entry:
                body_state = self.states[body_entry]
                self.states[entry].transitions = copy.deepcopy(body_state.transitions)
                self.states[entry].is_terminal = body_state.is_terminal
            return entry
        raise TypeError(f"Unsupported local protocol AST node: {type(node)!r}")

    @staticmethod
    def _split_label_type(raw: str) -> tuple[str, Optional[str]]:
        if "__" not in raw:
            return raw, None
        label, data_type = raw.split("__", 1)
        return label, data_type

    def clone(self) -> "LocalProtocol":
        return LocalProtocol(self.protocol_text, self.role_name)

    def get_current_position(self) -> ProtocolState:
        return self.states[self.current_position]

    def get_expected_transitions(self) -> list[ProtocolTransition]:
        return list(self.get_current_position().transitions)

    def expected_transition(
        self,
        direction: Optional[str] = None,
        peer: Optional[str] = None,
    ) -> Optional[ProtocolTransition]:
        transitions = self.get_expected_transitions()
        if direction:
            transitions = [t for t in transitions if t.action.value == direction]
        if peer:
            transitions = [
                t for t in transitions if t.peer.lower() == peer.lower()
            ]
        return transitions[0] if len(transitions) == 1 else None

    def validate(
        self,
        *,
        direction: str,
        peer: Optional[str],
        label: str,
        value: Any,
    ) -> tuple[bool, Optional[str], Optional[ViolationCode]]:
        state = self.get_current_position()
        if state.is_terminal:
            return False, "Protocol is already complete", ViolationCode.WRONG_ORDER

        action_matches = [t for t in state.transitions if t.action.value == direction]
        if not action_matches:
            expected = sorted({t.action.value for t in state.transitions})
            return (
                False,
                f"Expected action {expected}, got {direction}",
                ViolationCode.WRONG_DIRECTION,
            )

        peer_matches = [t for t in action_matches if peer is None or t.peer.lower() == peer.lower()]
        if not peer_matches:
            expected = sorted({t.peer for t in action_matches})
            return False, f"Expected peer {expected}, got {peer!r}", ViolationCode.WRONG_PEER

        label_matches = [t for t in peer_matches if t.label.lower() == label.lower()]
        if not label_matches:
            expected = sorted({t.label for t in peer_matches})
            return False, f"Expected label {expected}, got {label!r}", ViolationCode.WRONG_LABEL

        transition = label_matches[0]
        if transition.data_type:
            valid, error = validate_value_type(value, transition.data_type)
            if not valid:
                return False, error, ViolationCode.WRONG_TYPE

        old_state = self.current_position
        self.current_position = transition.target
        self.position_history.append(self.current_position)
        logger.info("Protocol transition: %s -> %s", old_state, self.current_position)
        return True, None, None

    def is_complete(self) -> bool:
        if self.get_current_position().is_terminal:
            return True
        # Returning to the initial state is a legal cycle boundary, including
        # subset-projection FSMs where the textual output no longer contains μ.
        return bool(self.position_history) and self.current_position == self.initial_position

    def finalize(self) -> tuple[bool, Optional[str]]:
        if self.is_complete():
            return True, None
        state = self.get_current_position()
        expected = [transition.to_dict() for transition in state.transitions]
        return False, f"Protocol ended before completion; expected one of {expected}"

    def reset(self) -> None:
        self.current_position = self.initial_position
        self.position_history = []

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role_name,
            "initial_position": self.initial_position,
            "current_position": self.current_position,
            "recursive": self.recursive,
            "complete": self.is_complete(),
            "states": {name: state.to_dict() for name, state in self.states.items()},
            "positions": {name: state.to_dict() for name, state in self.states.items()},
            "position_history": list(self.position_history),
        }


class MPSTValidator:
    """Runtime validator for one protocol session."""

    def __init__(self, local_protocol: Optional[LocalProtocol] = None):
        self.protocol = local_protocol
        self.violations: list[dict[str, Any]] = []

    def set_protocol(self, protocol_text: str, role_name: str) -> bool:
        try:
            self.protocol = LocalProtocol(protocol_text, role_name)
            self.violations = []
            return True
        except Exception:
            logger.exception("Failed to initialize MPST protocol for role %s", role_name)
            self.protocol = None
            return False

    def expected_transition(
        self,
        direction: Optional[str] = None,
        peer: Optional[str] = None,
    ) -> Optional[ProtocolTransition]:
        if not self.protocol:
            return None
        return self.protocol.expected_transition(direction, peer)

    def validate_tool_call_completion(
        self,
        content: Any,
        generation_metadata: Optional[Mapping[str, Any]] = None,
    ) -> dict[str, Any]:
        """Reject tool calls that escaped the agent's internal execution loop.

        This check runs before protocol-label wrapping and before the protocol
        state is advanced. The executor may therefore ask the same internal
        agent session to regenerate without corrupting the MPST session state.
        """
        if not self.protocol:
            return self._result(
                False,
                "No protocol initialized",
                ViolationCode.PROTOCOL_NOT_INITIALIZED,
            )

        metadata = dict(generation_metadata or {})
        tool_required = bool(metadata.get("tool_required"))
        call_observed = bool(metadata.get("tool_call_observed"))
        response_observed = bool(metadata.get("tool_response_observed"))
        unexecuted_call = bool(metadata.get("unexecuted_tool_call"))
        tool_name = str(metadata.get("tool_name") or "").strip()

        error: Optional[str] = None
        if unexecuted_call:
            suffix = f" '{tool_name}'" if tool_name else ""
            error = f"Unexecuted tool call{suffix} reached the final agent output"
        elif self._contains_tool_call_payload(content, tool_name=tool_name):
            error = "Tool-call syntax leaked into the final agent output"
        elif tool_required and not response_observed:
            error = "The agent produced a final response before a required tool completed"
        elif call_observed and not response_observed:
            error = "A tool call was observed without a corresponding tool response"

        if error is None:
            result = self._result(True, None, None, value=content)
            result["retryable"] = False
            return result

        violation = {
            "code": ViolationCode.TOOL_CALL_INCOMPLETE.value,
            "message": self._content_text(content),
            "direction": "send",
            "error": error,
            "position": self.protocol.current_position,
            "retryable": True,
            "tool_name": tool_name or None,
        }
        self.violations.append(violation)
        logger.warning("MPST tool-call violation: %s", violation)
        result = self._result(
            False,
            error,
            ViolationCode.TOOL_CALL_INCOMPLETE,
            value=content,
        )
        result["retryable"] = True
        result["tool_name"] = tool_name or None
        return result

    def validate_message(
        self,
        message_content: Any,
        direction: str,
        sender: Optional[str] = None,
        receiver: Optional[str] = None,
        message_value: Any = None,
        message_label: Optional[str] = None,
        generation_metadata: Optional[Mapping[str, Any]] = None,
        check_tool_call: bool = True,
    ) -> dict[str, Any]:
        if not self.protocol:
            return self._result(
                False,
                "No protocol initialized",
                ViolationCode.PROTOCOL_NOT_INITIALIZED,
            )

        if direction == MessageType.SEND.value and check_tool_call:
            tool_check = self.validate_tool_call_completion(
                message_content,
                generation_metadata,
            )
            if not tool_check["is_valid"]:
                return tool_check

        content_text = message_content if isinstance(message_content, str) else json.dumps(message_content, ensure_ascii=False)
        label = message_label or self._extract_message_label(content_text)
        value = message_value if message_value is not None else self._extract_message_value(content_text)
        peer = receiver if direction == "send" else sender
        is_valid, error, code = self.protocol.validate(
            direction=direction,
            peer=peer,
            label=label,
            value=value,
        )
        result = self._result(is_valid, error, code, label=label, value=value)
        if not is_valid:
            violation = {
                "code": code.value if code else None,
                "message": content_text,
                "direction": direction,
                "peer": peer,
                "label": label,
                "error": error,
                "position": self.protocol.current_position,
            }
            self.violations.append(violation)
            logger.warning("MPST violation: %s", violation)
        return result

    @classmethod
    def contains_tool_call_payload(
        cls,
        content: Any,
        *,
        tool_name: str = "",
    ) -> bool:
        """Return whether content exposes an unexecuted tool-call payload."""
        if isinstance(content, Mapping):
            lowered_keys = {str(key).lower() for key in content}
            if lowered_keys.intersection({"tool_call", "tool_calls", "function_call"}):
                return True
            if "name" in lowered_keys and lowered_keys.intersection({"args", "arguments"}):
                return True
            return any(
                cls.contains_tool_call_payload(value, tool_name=tool_name)
                for value in content.values()
            )
        if isinstance(content, (list, tuple)):
            return any(
                cls.contains_tool_call_payload(item, tool_name=tool_name)
                for item in content
            )

        text = cls._content_text(content).strip()
        if not text:
            return False

        lowered = text.lower()
        markers = (
            "<tool_call",
            "</tool_call",
            '"tool_call"',
            '"tool_calls"',
            '"function_call"',
            "assistant to=",
            "error: tool call not executed",
        )
        if any(marker in lowered for marker in markers):
            return True
        if re.search(
            r"(?im)^\s*tool calls?\s*:\s*(?:```(?:json)?\s*)?[\[{]",
            text,
        ):
            return True

        if tool_name and re.search(
            rf"(?is)(?:^|[\s`]){re.escape(tool_name)}\s*\(",
            text,
        ):
            return True

        candidate = text
        if candidate.startswith("```") and candidate.endswith("```"):
            candidate = re.sub(r"^```(?:json)?\s*", "", candidate, flags=re.IGNORECASE)
            candidate = re.sub(r"\s*```$", "", candidate)
        try:
            parsed = json.loads(candidate)
        except (json.JSONDecodeError, TypeError, ValueError):
            return False
        if isinstance(parsed, (Mapping, list, tuple)):
            return cls.contains_tool_call_payload(
                parsed,
                tool_name=tool_name,
            )
        return False

    @classmethod
    def _contains_tool_call_payload(
        cls,
        content: Any,
        *,
        tool_name: str = "",
    ) -> bool:
        """Compatibility wrapper for existing validator integrations."""
        return cls.contains_tool_call_payload(content, tool_name=tool_name)

    @staticmethod
    def _content_text(content: Any) -> str:
        if isinstance(content, str):
            return content
        try:
            return json.dumps(content, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            return str(content)

    def finalize(self) -> dict[str, Any]:
        if not self.protocol:
            return self._result(False, "No protocol initialized", ViolationCode.PROTOCOL_NOT_INITIALIZED)
        is_valid, error = self.protocol.finalize()
        code = None if is_valid else ViolationCode.INCOMPLETE_PROTOCOL
        result = self._result(is_valid, error, code)
        if not is_valid:
            self.violations.append({
                "code": code.value,
                "error": error,
                "position": self.protocol.current_position,
                "direction": "finalize",
            })
        return result

    def _result(
        self,
        is_valid: bool,
        error: Optional[str],
        code: Optional[ViolationCode],
        *,
        label: Optional[str] = None,
        value: Any = None,
    ) -> dict[str, Any]:
        status = self.get_status()
        return {
            "is_valid": is_valid,
            "error": error,
            "code": code.value if code else None,
            "message_label": label,
            "message_value": value,
            **status,
        }

    @staticmethod
    def _extract_message_label(message_content: str) -> str:
        bracket = re.search(r"\[([A-Za-z_]\w*)\s*:\s*[\s\S]*\]", message_content)
        if bracket:
            return bracket.group(1).lower()
        colon = re.match(r"\s*([A-Za-z_]\w*)\s*:", message_content)
        if colon:
            return colon.group(1).lower()
        words = re.findall(r"[A-Za-z_]\w*", message_content)
        return words[0].lower() if words else ""

    @staticmethod
    def _extract_message_value(message_content: str) -> Optional[str]:
        bracket = re.search(r"\[[A-Za-z_]\w*\s*:\s*([\s\S]*)\]", message_content)
        if bracket:
            return bracket.group(1).strip()
        colon = re.match(r"\s*[A-Za-z_]\w*\s*:\s*([\s\S]*)", message_content)
        if colon:
            return colon.group(1).strip()
        return message_content.strip() or None

    def get_status(self) -> dict[str, Any]:
        if not self.protocol:
            return {
                "initialized": False,
                "enabled": False,
                "current_position": None,
                "expected_transitions": [],
                "position_history": [],
                "violations": list(self.violations),
            }
        state = self.protocol.get_current_position()
        return {
            "initialized": True,
            "enabled": True,
            "current_position": state.name,
            "expected_transitions": [t.to_dict() for t in state.transitions],
            "position_history": list(self.protocol.position_history),
            "complete": self.protocol.is_complete(),
            "violations": list(self.violations),
        }

    def reset(self) -> None:
        if self.protocol:
            self.protocol.reset()
        self.violations = []


class ValidatorRegistry:
    """Protocol templates plus isolated validator state for each A2A session."""

    def __init__(self, role_name: str):
        self.role_name = role_name
        self._templates: dict[str, str] = {}
        self._sessions: dict[tuple[str, str], MPSTValidator] = {}
        self.default_protocol_id: Optional[str] = None

    def register_protocol(self, protocol_id: str, protocol_text: str) -> bool:
        probe = MPSTValidator()
        if not probe.set_protocol(protocol_text, self.role_name):
            return False
        self._templates[protocol_id] = protocol_text
        self.default_protocol_id = protocol_id
        # A changed protocol must not reuse state created from an older template.
        self._sessions = {
            key: validator for key, validator in self._sessions.items() if key[1] != protocol_id
        }
        return True

    def has_protocol(self) -> bool:
        return bool(self._templates)

    def get(self, session_id: str, protocol_id: Optional[str] = None) -> MPSTValidator:
        selected = protocol_id or self.default_protocol_id
        if not selected or selected not in self._templates:
            raise KeyError("No protocol template is registered")
        key = (session_id, selected)
        validator = self._sessions.get(key)
        if validator is None:
            validator = MPSTValidator()
            if not validator.set_protocol(self._templates[selected], self.role_name):
                raise ValueError(f"Failed to instantiate protocol {selected!r}")
            self._sessions[key] = validator
        return validator

    def status(self, session_id: Optional[str] = None) -> dict[str, Any]:
        if session_id and self.default_protocol_id:
            validator = self._sessions.get((session_id, self.default_protocol_id))
            if validator:
                return validator.get_status()
        return {
            "initialized": self.has_protocol(),
            "role": self.role_name,
            "protocols": sorted(self._templates),
            "active_sessions": len(self._sessions),
        }

    def reset_session(self, session_id: str) -> None:
        for key in [key for key in self._sessions if key[0] == session_id]:
            del self._sessions[key]
