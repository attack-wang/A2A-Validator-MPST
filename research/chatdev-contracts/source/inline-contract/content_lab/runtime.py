"""Finite protocol guard + pure content checks + one in-memory commit point.

This is an experimental finite-state adapter, not an MPST projection engine.
Plugins are trusted local Python code; copying inputs is not a security sandbox.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from threading import RLock
from typing import Any, Callable


@dataclass(frozen=True)
class Violation:
    layer: str
    rule: str
    path: str
    message: str
    repair: str


@dataclass(frozen=True)
class Message:
    sender: str
    receiver: str
    label: str
    payload: Any


@dataclass(frozen=True)
class Decision:
    accepted: bool
    state_before: str
    state_after: str
    attempt: int
    retry_allowed: bool
    violations: tuple[Violation, ...]

    def to_dict(self) -> dict:
        return asdict(self)


Check = Callable[[Any, dict], list[Violation]]


class Runtime:
    def __init__(self, protocol: dict, contracts: dict, checks: dict[str, Check],
                 artifacts: dict, *, content_enabled: bool = True):
        self._protocol = deepcopy(protocol)
        self._contracts = deepcopy(contracts)
        self._checks = dict(checks)
        self._artifacts = deepcopy(artifacts)
        self._content_enabled = content_enabled
        self._state = protocol["initial"]
        self._history: list[Message] = []
        self._audit: list[dict] = []
        self._attempts: dict[tuple, int] = {}
        self._lock = RLock()
        for name, contract in self._contracts.items():
            if type(contract.get("max_attempts")) is not int or contract["max_attempts"] < 1:
                raise ValueError(f"Invalid max_attempts: {name}")
            if not contract.get("checks") or any(c not in checks for c in contract["checks"]):
                raise ValueError(f"Missing or empty checks: {name}")
        for transition in self._protocol["transitions"]:
            if transition.get("payload_type") not in {"object", "text"}:
                raise ValueError("Unsupported payload_type")
            name = transition.get("contract")
            if name and name not in self._contracts:
                raise ValueError(f"Unknown contract: {name}")

    @property
    def state(self) -> str:
        with self._lock:
            return self._state

    @property
    def history(self) -> list[Message]:
        with self._lock:
            return deepcopy(self._history)

    @property
    def audit(self) -> list[dict]:
        with self._lock:
            return deepcopy(self._audit)

    @property
    def artifacts(self) -> dict:
        with self._lock:
            return deepcopy(self._artifacts)

    def submit(self, candidate: Message) -> Decision:
        """Validate private snapshots; atomically append delivery and advance state.

        Rejection changes only attempt counters and diagnostic audit. History,
        artifacts and protocol state remain unchanged. No external delivery occurs.
        """
        with self._lock:
            message = deepcopy(candidate)
            before = self._state
            transition = next((t for t in self._protocol["transitions"]
                               if t["state"] == before and t["sender"] == message.sender
                               and t["receiver"] == message.receiver and t["label"] == message.label), None)
            if transition is None:
                return self._record(message, before, 0, False, [Violation(
                    "G0", "protocol_transition", "$", "Message is not enabled in the current state.",
                    "Use the sender, receiver and label enabled by the protocol.")])
            expected = dict if transition["payload_type"] == "object" else str
            if not isinstance(message.payload, expected):
                return self._record(message, before, 0, False, [Violation(
                    "G0", "payload_type", "payload", f"Expected {transition['payload_type']}.",
                    "Supply the protocol payload type.")])
            name = transition.get("contract") if self._content_enabled else None
            contract = self._contracts.get(name) if name else None
            key = (len(self._history), before, message.sender, message.receiver, message.label)
            attempt = self._attempts.get(key, 0) + 1
            if contract and attempt > contract["max_attempts"]:
                return self._record(message, before, attempt, False, [Violation(
                    "policy", "attempt_limit", "$", "Content repair attempts exhausted.",
                    "Escalate for review or start a new experimental session.")])
            self._attempts[key] = attempt
            violations: list[Violation] = []
            if contract:
                context = {"artifacts": self._artifacts, "history": self._history,
                           "state": before, "contract": name}
                for check_name in contract["checks"]:
                    try:
                        findings = self._checks[check_name](deepcopy(message.payload), deepcopy(context))
                        if not isinstance(findings, list) or any(not isinstance(v, Violation) for v in findings):
                            raise TypeError("Check must return a list of Violation")
                        violations.extend(findings)
                    except Exception as error:
                        violations.append(Violation("runtime", check_name, "$",
                                                    f"Validator failed: {type(error).__name__}.",
                                                    "Inspect the validator; do not accept this message."))
                    # Later checks can assume successful earlier schema validation.
                    if violations:
                        break
            if violations:
                retry = bool(contract and attempt < contract["max_attempts"])
                return self._record(message, before, attempt, retry, violations)
            # The only commit point. Delivery means appending to this local history.
            self._history.append(message)
            self._state = transition["target"]
            return self._record(message, before, attempt, False, [])

    def _record(self, message: Message, before: str, attempt: int,
                retry: bool, violations: list[Violation]) -> Decision:
        decision = Decision(not violations, before, self._state, attempt, retry, tuple(violations))
        self._audit.append({"message": asdict(message), "decision": decision.to_dict()})
        return decision
