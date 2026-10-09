from __future__ import annotations

import copy
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

def _find_repo_root() -> Path:
    configured = os.environ.get('MPST_A2A_ROOT')
    # Prefer the isolated source tree even if the parent shell points to the original repo.
    candidates = list(Path(__file__).resolve().parents) + ([Path(configured).expanduser()] if configured else [])
    for candidate in candidates:
        if (candidate / 'mpst-runtime' / 'mpst_ext' / 'mpst_ext').is_dir() and (
            candidate / 'host-platform' / 'backend' / 'python' / 'hosts' / 'multiagent'
        ).is_dir():
            return candidate
    raise RuntimeError(
        'Cannot locate mpst-a2a-validator runtime. Set MPST_A2A_ROOT to the directory '
        'containing mpst-runtime and host-platform.'
    )


_REPO_ROOT = _find_repo_root()
_MPST_PATH = _REPO_ROOT / 'mpst-runtime' / 'mpst_ext' / 'mpst_ext'
_HOST_PATH = _REPO_ROOT / 'host-platform' / 'backend' / 'python' / 'hosts' / 'multiagent'
for path in (_MPST_PATH, _HOST_PATH):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from gt_projection import GTProjection  # noqa: E402
from mpst_validator import MPSTValidator  # noqa: E402

logger = logging.getLogger(__name__)


class ProtocolViolationError(RuntimeError):
    """Raised when a ChatDev edge is outside the projected session type."""

    def __init__(self, message: str, violation: Optional[dict[str, Any]] = None):
        super().__init__(message)
        self.violation = violation


def _normalized(value: object) -> str:
    return re.sub(r'[^a-z0-9]', '', str(value or '').lower())


def _message_text(message: object) -> str:
    text_content = getattr(message, 'text_content', None)
    if callable(text_content):
        return text_content()
    return str(getattr(message, 'content', '') or '')


class ChatDevSessionTypeMonitor:
    """Validate ChatDev edge transmissions with projected local MPST protocols."""

    DEFAULT_PROTOCOL = Path(__file__).resolve().parent / 'protocol' / 'chatdev_codegen.gt'
    DEFAULT_ROLES = {
        'User': ('user',),
        'Programmer': ('programmer',),
        'CodeReviewer': ('codereviewer',),
        'SoftwareTestEngineer': ('softwaretestengineer',),
        'ChiefProductOfficer': ('chiefproductofficer',),
        'ChiefExecutiveOfficer': ('chiefexecutiveofficer',),
    }

    def __init__(
        self,
        protocol_path: str | Path | None = None,
        role_map: Optional[dict[str, str]] = None,
        projection_method: str = 'subset',
        strict_unmapped: bool = True,
        max_retries: int = 2,
        use_default_roles: bool = True,
        contract_validator=None,
    ) -> None:
        self.protocol_path = Path(protocol_path or self.DEFAULT_PROTOCOL)
        if not self.protocol_path.exists():
            raise FileNotFoundError(self.protocol_path)
        self.role_map = dict(role_map or {})
        self.strict_unmapped = strict_unmapped
        self.use_default_roles = use_default_roles
        if max_retries < 0:
            raise ValueError('max_retries must be non-negative')
        self.max_retries = max_retries
        self.contract_validator = contract_validator
        self.contract_bindings = {}
        projection = GTProjection(projection_method)
        protocol_name = self.protocol_path.stem
        roles = projection.get_all_roles(str(self.protocol_path))
        if not roles:
            raise ValueError(f'No roles found in {self.protocol_path}')
        self.validators: dict[str, MPSTValidator] = {}
        for role in roles:
            projected = projection.project_protocol(
                str(self.protocol_path),
                protocol_name,
                role,
            )
            if not projected.get('local_protocol'):
                raise ValueError(projected.get('error') or f'Cannot project protocol onto {role}')
            validator = MPSTValidator()
            if not validator.set_protocol(projected['local_protocol'], role):
                raise ValueError(f'Cannot initialize MPST protocol for {role}')
            from content_lab.protocol_annotations import bind_projected_transitions
            bindings = projected.get('contract_bindings', {})
            bind_projected_transitions(validator.protocol, bindings, role)
            self.contract_bindings.update(bindings)
            self.validators[role] = validator
        self.violations: list[dict[str, Any]] = []

    def reset(self) -> None:
        self.violations.clear()
        for validator in self.validators.values():
            validator.reset()

    @property
    def is_terminated(self) -> bool:
        return all(validator.protocol.is_complete() for validator in self.validators.values())

    @property
    def session_type_violations(self) -> list[dict[str, Any]]:
        return list(self.violations)

    @property
    def unresolved_violations(self) -> list[dict[str, Any]]:
        return [violation for violation in self.violations if not violation.get('resolved', False)]

    def snapshot_state(self) -> dict[str, MPSTValidator]:
        """Copy protocol positions so a rejected node attempt can be rolled back."""
        return copy.deepcopy(self.validators)

    def restore_state(self, snapshot: dict[str, MPSTValidator]) -> None:
        """Restore protocol positions while retaining violation diagnostics."""
        self.validators = copy.deepcopy(snapshot)

    def can_retry(self, violation: Optional[dict[str, Any]]) -> bool:
        return bool(violation) and int(violation.get('attempt', 1)) <= self.max_retries

    def retry_feedback(self, violation: Optional[dict[str, Any]]) -> str:
        violation = violation or {}
        source = str(violation.get('source', 'unmapped'))
        target = str(violation.get('target', 'unmapped'))
        expected = violation.get('expected')
        if expected is None and source in self.validators:
            expected = self.expected_transitions(source)
        attempt = int(violation.get('attempt', 1))
        return (
            f"Session-type validation rejected the previous delivery from {source} to {target}. "
            "The protocol and message queues were rolled back. Regenerate the response so it "
            f"selects one of these allowed transitions: {expected or []}. "
            f"Retry {attempt} of {self.max_retries}."
        )

    def _resolve_source_violations(self, source: str) -> None:
        for violation in self.violations:
            if violation.get('source') == source and not violation.get('resolved', False):
                violation['resolved'] = True

    def _role_candidates(self, node: object) -> list[str]:
        return [
            str(getattr(node, 'id', '') or ''),
            str(getattr(node, 'role', '') or ''),
            str(getattr(node, 'description', '') or ''),
        ]

    def _role_for(self, node: object) -> Optional[str]:
        explicit = self.role_map.get(str(getattr(node, 'id', '') or ''))
        if explicit:
            return explicit
        if not self.use_default_roles:
            return None
        candidates = {_normalized(item) for item in self._role_candidates(node)}
        for role, aliases in self.DEFAULT_ROLES.items():
            if role not in self.validators:
                continue
            alias_candidates = {role, *aliases}
            if any(candidate in alias_candidates for candidate in candidates):
                return role
            if any(alias in candidate for candidate in candidates for alias in alias_candidates):
                return role
        return None

    def _transition(self, source: str, target: str, label=None, interaction_id=None) -> tuple[Optional[str], Optional[dict[str, Any]]]:
        validator = self.validators.get(source)
        if validator is None:
            return None, None
        candidates = [t for t in validator.protocol.get_expected_transitions()
                      if t.action.value == 'send' and t.peer == target
                      and (label is None or t.label == label.lower())
                      and (interaction_id is None or t.interaction_id == interaction_id)]
        incoming = self.validators[target].protocol.get_expected_transitions()
        candidates = [t for t in candidates if any(
            r.action.value == 'receive' and r.peer == source and r.label == t.label
            and r.interaction_id == t.interaction_id and r.contract_ref == t.contract_ref
            for r in incoming)]
        if not candidates:
            return None, None
        policies = {(t.label, t.contract_ref, t.payload_schema) for t in candidates}
        if len(policies) != 1:
            raise ProtocolViolationError('Ambiguous enabled messages/contracts; supply label/interaction_id')
        transition = candidates[0]
        return transition.label, transition.to_dict()

    def transition_for(self, source, target, label):
        _, transition = self._transition(source, target, label)
        if transition is None:
            raise ProtocolViolationError(f'No enabled transition {source} -> {target}:{label}')
        return transition

    def validate_candidate(self, source, target, label, payload, generation=None):
        transition = self.transition_for(source, target, label)
        reference = transition.get('contract_ref')
        if reference:
            if self.contract_validator is None:
                raise ProtocolViolationError('Annotated transition has no contract executor')
            self.contract_validator(reference, payload, transition, generation)
        return transition

    def check(self, edge_link: object, message: object, from_node: object) -> dict[str, Any]:
        source = self._role_for(from_node)
        target = self._role_for(edge_link.target)
        if not source or not target:
            if not self.strict_unmapped:
                return {'skipped': True, 'reason': 'unmapped_role'}
            violation = self._record(source or 'unmapped', target or 'unmapped', 'unmapped_role')
            raise ProtocolViolationError(
                f'Unmapped ChatDev edge {from_node.id} -> {edge_link.target.id}',
                violation=violation,
            )
        label, transition = self._transition(source, target, getattr(message, 'message_label', None),
                                             getattr(message, 'interaction_id', None))
        if transition is None or label is None:
            violation = self._record(
                source, target, 'invalid_transition', expected=self._expected(source)
            )
            raise ProtocolViolationError(
                f'{source} may not send to {target}', violation=violation
            )
        content = _message_text(message)
        sender_validator = copy.deepcopy(self.validators[source])
        recipient_validator = copy.deepcopy(self.validators[target])
        # Equal public labels in separate branches retain their interaction IDs.
        # Select the same projected communication on both sides before advancing.
        original_alternatives = []
        if transition.get('interaction_id'):
            for validator in (sender_validator, recipient_validator):
                state = validator.protocol.get_current_position()
                original_alternatives.append((state, state.transitions))
                state.transitions = [t for t in state.transitions
                                     if t.interaction_id == transition['interaction_id']]
        sender_result = sender_validator.validate_message(
            content,
            direction='send',
            receiver=target,
            message_label=label,
            check_tool_call=False,
        )
        if not sender_result['is_valid']:
            violation = self._record(
                source, target, sender_result.get('code'), result=sender_result
            )
            raise ProtocolViolationError(
                sender_result.get('error') or 'MPST violation', violation=violation
            )
        recipient_result = recipient_validator.validate_message(
            content,
            direction='receive',
            sender=source,
            message_label=label,
            check_tool_call=False,
        )
        if not recipient_result['is_valid']:
            violation = self._record(
                source, target, recipient_result.get('code'), result=recipient_result
            )
            raise ProtocolViolationError(
                recipient_result.get('error') or 'MPST violation', violation=violation
            )
        for state, alternatives in original_alternatives:
            state.transitions = alternatives
        if transition.get('contract_ref'):
            if self.contract_validator is None:
                raise ProtocolViolationError('Annotated transition has no contract executor')
            self.contract_validator(transition['contract_ref'], content, transition, None)
        self.validators[source] = sender_validator
        self.validators[target] = recipient_validator
        self._resolve_source_violations(source)
        return transition

    def observe(self, edge_link: object, message: object, from_node: object) -> bool:
        source = self._role_for(from_node)
        target = self._role_for(edge_link.target)
        if not source or not target:
            if not self.strict_unmapped:
                return True
            self._record(source or 'unmapped', target or 'unmapped', 'unmapped_role')
            logger.warning(
                'session-type violation: unmapped ChatDev edge %s -> %s',
                getattr(from_node, 'id', ''),
                getattr(edge_link.target, 'id', ''),
            )
            return False
        try:
            self.check(edge_link, message, from_node)
            return True
        except ProtocolViolationError as exc:
            logger.warning('session-type violation: %s', exc)
            return False

    def _expected(self, role: str) -> list[dict[str, Any]]:
        return self.expected_transitions(role)

    def expected_transitions(self, role: str) -> list[dict[str, Any]]:
        validator = self.validators.get(role)
        if validator is None:
            return []
        return [transition.to_dict() for transition in validator.protocol.get_expected_transitions()]

    def _record(self, source: str, target: str, code: object, **details: object) -> dict[str, Any]:
        attempt = 1 + sum(
            1
            for item in self.violations
            if item.get('source') == source and not item.get('resolved', False)
        )
        violation = {
            'source': source,
            'target': target,
            'code': str(code) if code else None,
            'attempt': attempt,
            'resolved': False,
            **details,
        }
        self.violations.append(violation)
        logger.warning('MPST violation: %s', violation)
        return violation
