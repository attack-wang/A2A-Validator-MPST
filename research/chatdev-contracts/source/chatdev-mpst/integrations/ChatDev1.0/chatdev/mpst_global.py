"""Global, coordinator-mediated MPST protocol for the ChatDev 1.0 pilot.

This observes the order in which ChatChain dispatches phases and receives
their replies. The TestErrorSummary phase also records the test engineer's
report before sending it to the programmer. It does not inspect whether the
generated code satisfies the task; artifact evaluation remains separate.
"""

from pathlib import Path
from types import SimpleNamespace

from chatdev.mpst_pilot import ChatDevSessionTypeMonitor


_PROTOCOL = Path(__file__).resolve().parents[1] / "protocol" / "mpst_global_pilot.gt"
_ROLES = (
    "Coordinator", "ChiefProductOfficer", "ChiefTechnologyOfficer",
    "Programmer", "CodeReviewer", "SoftwareTestEngineer", "WorkflowEnd",
)
_PHASE_EVENTS = {
    "DemandAnalysis": ("ChiefProductOfficer", "demand", "demandResult"),
    "LanguageChoose": ("ChiefTechnologyOfficer", "language", "languageResult"),
    "Coding": ("Programmer", "coding", "codingResult"),
    "CodeComplete": ("Programmer", "codeComplete", "codeCompleteResult"),
    "CodeReviewComment": ("CodeReviewer", "review", "reviewResult"),
    "CodeReviewModification": ("Programmer", "reviewFix", "reviewFixResult"),
    "TestErrorSummary": ("Programmer", "testSummary", "testSummaryResult"),
    "TestModification": ("Programmer", "testFix", "testFixResult"),
}


class GlobalPilotMonitor:
    def __init__(self):
        self.monitor = ChatDevSessionTypeMonitor(
            protocol_path=_PROTOCOL,
            role_map={role: role for role in _ROLES},
            use_default_roles=False,
            max_retries=2,
        )
        self.checked_phases = 0

    def snapshot(self):
        return self.monitor.snapshot_state(), self.checked_phases

    def restore(self, snapshot):
        validators, count = snapshot
        self.monitor.restore_state(validators)
        self.checked_phases = count

    def _advance(self, source, target, label, content):
        expected = self.monitor.expected_transitions(source)
        if not any(
            item.get("action") == "send"
            and item.get("peer") == target
            and str(item.get("label", "")).lower() == label.lower()
            for item in expected
        ):
            raise RuntimeError(
                "Global MPST rejected {} -> {}:{}; expected {}".format(
                    source, target, label, expected
                )
            )
        return self.monitor.check(
            SimpleNamespace(target=SimpleNamespace(id=target)),
            SimpleNamespace(content=str(content or "")),
            SimpleNamespace(id=source),
        )

    def begin_phase(self, phase_name, request_content, phase_env=None):
        if phase_name not in _PHASE_EVENTS:
            raise RuntimeError("Unmapped ChatDev 1.0 phase: " + phase_name)
        if phase_name == "TestErrorSummary":
            report = (phase_env or {}).get("test_reports", "")
            self._advance("Coordinator", "SoftwareTestEngineer", "test", report)
            self._advance("SoftwareTestEngineer", "Coordinator", "testReport", report)
        role, request_label, _ = _PHASE_EVENTS[phase_name]
        self._advance("Coordinator", role, request_label, request_content)

    def end_phase(self, phase_name, response_content):
        role, _, response_label = _PHASE_EVENTS[phase_name]
        self._advance(role, "Coordinator", response_label, response_content)
        self.checked_phases += 1

    def finish(self):
        self._advance("Coordinator", "WorkflowEnd", "done", "workflow complete")
        self._advance("WorkflowEnd", "Coordinator", "doneAck", "ack")
        # Subset projection retains dormant alternatives for roles not chosen
        # by the coordinator (for example no Test phase). The coordinator and
        # WorkflowEnd reaching 0 is the unambiguous completion criterion.
        if not all(
            self.monitor.validators[role].protocol.is_complete()
            for role in ("Coordinator", "WorkflowEnd")
        ):
            raise RuntimeError("Global MPST coordinator did not terminate")


class GlobalPhaseExchange:
    """Adapter allowing the existing empty-response retry helper to be reused."""

    def __init__(self, global_monitor, phase_name, phase_env):
        self.global_monitor = global_monitor
        self.phase_name = phase_name
        self.phase_env = phase_env
        self._complete = False

    def snapshot(self):
        return self.global_monitor.snapshot()

    def restore(self, snapshot):
        self.global_monitor.restore(snapshot)
        self._complete = False

    def request(self, message):
        self.global_monitor.begin_phase(self.phase_name, message.content, self.phase_env)

    def response(self, message):
        self.global_monitor.end_phase(self.phase_name, message.content)
        self._complete = True

    @property
    def complete(self):
        return self._complete
