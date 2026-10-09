"""Phase transaction adapter for copied ChatDev and the content-contract lab."""
from copy import deepcopy
import json
from pathlib import Path
import sys

_LAB = Path(__file__).resolve().parents[3]
if str(_LAB) not in sys.path:
    sys.path.insert(0, str(_LAB))

from content_lab.chatdev_contracts import (ChatDevContracts, ContentViolation, compile_checks,
                                         parse_json_response, smoke_run, snapshot, fail, startup_evidence)


class ChatDevContentGuard:
    def __init__(self, monitor, env):
        self.monitor = monitor
        self.env = env
        self.contracts = ChatDevContracts()
        from chatdev.mpst_global import _PHASE_EVENTS
        for name, binding in self.contracts.registry["phases"].items():
            role, _, label = _PHASE_EVENTS[name]
            if (binding["sender"], binding["receiver"], binding["label"]) != (role, "Coordinator", label):
                raise ValueError("Contract binding differs from ChatDev protocol: " + name)
        host_messages = self.contracts.registry["host_messages"]
        if (host_messages["testReport"]["sender"], host_messages["testReport"]["receiver"]) != ("SoftwareTestEngineer", "Coordinator"):
            raise ValueError("testReport binding differs from ChatDev protocol")
        if (host_messages["done"]["sender"], host_messages["done"]["receiver"]) != ("Coordinator", "WorkflowEnd"):
            raise ValueError("done binding differs from ChatDev protocol")
        if set(host_messages["done"]["requires"]) != {"current_source_compiles", "current_startup_passed"}:
            raise ValueError("Unsupported stage-exit requirements")
        self.last_review = None
        self.evidence = None
        self.delivered = []
        self._active_phase = 'host'
        self._active_phase_env = {}
        for binding in self.monitor.monitor.contract_bindings.values():
            reference = binding['contract_ref']
            if reference and reference not in self.contracts.definitions:
                raise ValueError('Unknown protocol contract reference: ' + reference)
            if reference and binding['payload_schema'] and (
                    binding['payload_schema'] != self.contracts.definitions[reference]['schema']):
                raise ValueError('Payload schema differs from contract: ' + reference)
        self.monitor.monitor.contract_validator = self._validate_protocol_message

    def context(self, phase, phase_env):
        return {"phase": phase, "phase_env": deepcopy(phase_env), "files": deepcopy(self.env.codes.codebooks),
                "last_review": deepcopy(self.last_review), "evidence": deepcopy(self.evidence)}

    def validate_candidate(self, phase, phase_env, text, generation=None):
        from chatdev.mpst_global import _PHASE_EVENTS
        self._active_phase, self._active_phase_env = phase, deepcopy(phase_env)
        role, _, label = _PHASE_EVENTS[phase]
        self.monitor.monitor.validate_candidate(role, 'Coordinator', label, text, generation)

    def _validate_protocol_message(self, reference, text, transition, generation=None):
        self.contracts.validate_contract(reference, text,
            self.context(self._active_phase, self._active_phase_env), generation, transition)

    def instruction(self, phase):
        if phase == "CodeReviewComment":
            return '\nContent contract: return one final JSON object. verdict must be finished or changes_requested. Example for a required repair: {"verdict":"changes_requested","issues":[{"file":"main.py","line":1,"message":"repair advice"}]}. Locations refer to supplied source; finished requires an empty issues list. Review occurs BEFORE startup testing. Do not claim tests passed.'
        if phase == "TestErrorSummary":
            return '\nContent contract: return only JSON with status, test_run_id and a nonempty summary. Copy status and test_run_id from this host startup record: ' + json.dumps(self.evidence, ensure_ascii=False)
        if phase == "LanguageChoose":
            return '\nThis experiment supports Python only. Return Python.'
        if phase in {"Coding", "CodeComplete", "CodeReviewModification", "TestModification"}:
            return '\nReturn FINAL SOURCE FILES ONLY. No analysis, architecture descriptions, examples, pseudocode or draft revisions. Each file must appear once as a standalone filename line followed by a closed ```python code block. Start with main.py for initial coding. Use a compact complete implementation within the output budget. No placeholder functions. Finished is allowed only if the supplied review/test evidence requires no repair.'
        return ''

    def prompt_for(self, phase):
        # ChatDev formats phase_prompt with str.format. Escape literal JSON in
        # the appended instruction while preserving native phase placeholders.
        from chatdev.mpst_global import _PHASE_EVENTS
        role, _, label = _PHASE_EVENTS[phase.phase_name]
        references = {b['contract_ref'] for b in self.monitor.monitor.contract_bindings.values()
                      if (b['sender'], b['receiver'], b['label']) == (role, 'Coordinator', label)}
        if not references or references == {None}:
            return phase.phase_prompt
        literal = self.instruction(phase.phase_name).replace('{', '{{').replace('}', '}}')
        return phase.phase_prompt + literal

    def capture_test(self):
        self.evidence = smoke_run(self.env.env_dict["directory"], self.env.codes.codebooks)
        checkpoint = self.monitor.snapshot()
        try:
            self.monitor._advance('Coordinator', 'SoftwareTestEngineer', 'test', 'host startup')
            transition = self.monitor.monitor.transition_for('SoftwareTestEngineer', 'Coordinator', 'testReport')
        finally:
            self.monitor.restore(checkpoint)
        if transition.get('contract_ref'):
            self._validate_protocol_message(transition['contract_ref'],
                json.dumps(self.evidence, ensure_ascii=False), transition)
        self.contracts.audit.append({'contract': transition.get('contract_ref'),
            'interaction_id': transition.get('interaction_id'), 'evidence': deepcopy(self.evidence),
            'accepted': True, 'trigger': 'projected_transition'})
        return self.evidence["status"] != "passed", json.dumps(self.evidence, ensure_ascii=False)

    def execute(self, phase, chat_turn_limit, need_reflect):
        if chat_turn_limit != 1 or need_reflect:
            raise ValueError("MPSTContent requires max_turn_step=1 and need_reflect=False")
        self._active_phase = phase.phase_name
        self._active_phase_env = phase.phase_env
        phase.update_phase_env(self.env)
        checkpoint = self.monitor.snapshot()
        before_files = snapshot(self.env.codes.codebooks)
        try:
            self.monitor.begin_phase(phase.phase_name, phase.phase_prompt, phase.phase_env)
            # RolePlaying validates the response BEFORE exposing it to the other role.
            phase.seminar_conclusion = phase.chatting(
                chat_env=self.env, task_prompt=self.env.env_dict['task_prompt'], need_reflect=False,
                assistant_role_name=phase.assistant_role_name, user_role_name=phase.user_role_name,
                phase_prompt=self.prompt_for(phase),
                phase_name=phase.phase_name, assistant_role_prompt=phase.assistant_role_prompt,
                user_role_prompt=phase.user_role_prompt, chat_turn_limit=1, placeholders=phase.phase_env,
                memory=self.env.memory, model_type=phase.model_type)
            if phase.phase_name in {'CodeReviewComment', 'TestErrorSummary'}:
                value = parse_json_response(phase.seminar_conclusion)
                if value is not None:
                    phase.seminar_conclusion = json.dumps(value, ensure_ascii=False)
            self.validate_candidate(phase.phase_name, phase.phase_env, phase.seminar_conclusion)
            self.monitor.end_phase(phase.phase_name, phase.seminar_conclusion)
            validated_protocol = self.monitor.snapshot()
        except Exception:
            self.monitor.restore(checkpoint)
            raise
        # Restore speculative G0 state until the accepted payload is applied.
        self.monitor.restore(checkpoint)
        previous_env = deepcopy(self.env.env_dict)
        previous_codes = deepcopy(self.env.codes.codebooks)
        previous_version = self.env.codes.version
        directory = Path(self.env.env_dict["directory"])
        previous_disk = {p.name: p.read_bytes() for p in directory.glob("*.py")}
        try:
            phase.update_chat_env(self.env)
        except Exception:
            self.env.env_dict = previous_env
            self.env.codes.codebooks = previous_codes
            self.env.codes.version = previous_version
            for path in directory.glob("*.py"):
                if path.name not in previous_disk:
                    path.unlink()
            for name, data in previous_disk.items():
                (directory / name).write_bytes(data)
            raise
        self.monitor.restore(validated_protocol)
        if phase.phase_name == "CodeReviewComment":
            self.last_review = parse_json_response(phase.seminar_conclusion)
        self.delivered.append({"phase": phase.phase_name, "source_snapshot": before_files["id"],
                               "result": phase.seminar_conclusion})
        return self.env

    def finish(self):
        self._active_phase, self._active_phase_env = 'exit', {}
        self.capture_test()  # a modification invalidates old execution evidence
        checkpoint = self.monitor.snapshot()
        try:
            self.monitor._advance("Coordinator", "SoftwareTestEngineer", "test", "final startup")
            self.monitor._advance("SoftwareTestEngineer", "Coordinator", "testReport", json.dumps(self.evidence))
            completion = self.monitor.monitor.transition_for('Coordinator', 'WorkflowEnd', 'done')
            self.monitor.finish()
        except Exception:
            self.monitor.restore(checkpoint)
            self.write_audit()
            raise
        self.contracts.audit.append({"contract": completion.get('contract_ref'), "accepted": True,
                                     "interaction_id": completion.get('interaction_id'),
                                     "trigger": 'projected_transition',
                                     "evidence_id": self.evidence["id"]})
        self.write_audit()

    def write_audit(self):
        directory = Path(self.env.env_dict["directory"])
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "content-contract-audit.json").write_text(json.dumps({
            "profile": self.contracts.registry["profile"], "delivered": self.delivered,
            "evidence": self.evidence, "checks": self.contracts.audit}, ensure_ascii=False, indent=2), encoding="utf-8")
