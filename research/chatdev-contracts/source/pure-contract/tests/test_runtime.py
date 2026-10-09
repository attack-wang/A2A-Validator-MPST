import unittest
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy

from content_lab.code_review import CHECKS
from content_lab.demo import ROOT, fixtures, make_runtime, run_demo
from content_lab.runtime import Message, Runtime
import json


class ContentContractTests(unittest.TestCase):
    def setUp(self):
        self.artifacts, self.report, self.review = fixtures()
        self.runtime = make_runtime()

    def changed(self, message, **fields):
        payload = deepcopy(message.payload)
        payload.update(fields)
        return Message(message.sender, message.receiver, message.label, payload)

    def rejection(self, message, rule):
        state, history, artifacts = self.runtime.state, self.runtime.history, self.runtime.artifacts
        decision = self.runtime.submit(message)
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.violations[0].rule, rule)
        self.assertEqual(self.runtime.state, state)
        self.assertEqual(self.runtime.history, history)
        self.assertEqual(self.runtime.artifacts, artifacts)
        return decision

    def test_protocol_only_accepts_false_approval(self):
        runtime = make_runtime(content_enabled=False)
        self.assertTrue(runtime.submit(self.report).accepted)
        self.assertTrue(runtime.submit(self.review).accepted)
        self.assertEqual(runtime.state, "done")

    def test_false_approval_leaves_state_and_delivery_unchanged(self):
        self.runtime.submit(self.report)
        self.assertTrue(self.rejection(self.review, "verdict_consistent").retry_allowed)

    def test_repaired_rejection_delivers_at_same_protocol_position(self):
        self.runtime.submit(self.report)
        self.runtime.submit(self.review)
        decision = self.runtime.submit(self.changed(self.review, verdict="reject", issues=[{
            "file": "calculator.py", "line": 2, "message": "Wrong operator."}]))
        self.assertTrue(decision.accepted)
        self.assertEqual(decision.attempt, 2)
        self.assertEqual(self.runtime.state, "done")
        self.assertEqual(len(self.runtime.history), 2)
        self.assertEqual(len(self.runtime.audit), 3)

    def test_forged_counts_detected_by_evidence(self):
        self.rejection(self.changed(self.report, passed=2, failed=0, status="passed"), "test_evidence")

    def test_stale_evidence_detected(self):
        self.artifacts["tests.v1"]["source_digests"] = {"calculator.py": "stale"}
        self.runtime = make_runtime(artifacts=self.artifacts)
        self.rejection(self.report, "test_version")

    def test_missing_evidence_detected(self):
        self.rejection(self.changed(self.report, test_run_id="invented"), "test_evidence")

    def test_source_digest_tampering_detected(self):
        self.artifacts["source.v1"]["files"]["calculator.py"] = "changed code"
        self.runtime = make_runtime(artifacts=self.artifacts)
        self.rejection(self.report, "test_evidence")

    def test_schema_requires_fields(self):
        payload = deepcopy(self.report.payload)
        del payload["failed"]
        self.rejection(Message("Tester", "Reviewer", "testReport", payload), "test_schema")

    def test_bool_is_not_an_integer_count(self):
        self.rejection(self.changed(self.report, passed=True), "test_schema")

    def test_counts_must_sum(self):
        self.rejection(self.changed(self.report, total=3), "test_counts")

    def test_empty_test_run_is_not_success(self):
        self.rejection(self.changed(self.report, passed=0, failed=0, total=0, status="passed"), "test_counts")

    def test_status_must_match_counts(self):
        self.rejection(self.changed(self.report, status="passed"), "test_status")

    def test_wrong_order(self):
        self.rejection(self.review, "protocol_transition")

    def test_wrong_roles_and_label(self):
        for message in (Message("Other", "Reviewer", "testReport", {}),
                        Message("Tester", "Other", "testReport", {}),
                        Message("Tester", "Reviewer", "unknown", {})):
            self.rejection(message, "protocol_transition")

    def test_wrong_payload_type(self):
        self.rejection(Message("Tester", "Reviewer", "testReport", "all passed"), "payload_type")

    def test_bad_issue_location(self):
        self.runtime.submit(self.report)
        for line in (0, 99):
            self.rejection(self.changed(self.review, verdict="reject", issues=[{
                "file": "calculator.py", "line": line, "message": "Wrong operator."}]), "issue_location")

    def test_cross_message_version(self):
        self.runtime.submit(self.report)
        self.rejection(self.changed(self.review, test_run_id="tests.v2", verdict="reject"), "history_version")

    def test_attempt_limit_blocks_even_repaired_message(self):
        self.runtime.submit(self.report)
        self.assertTrue(self.runtime.submit(self.review).retry_allowed)
        self.assertFalse(self.runtime.submit(self.review).retry_allowed)
        self.rejection(self.changed(self.review, verdict="reject"), "attempt_limit")

    def test_passing_evidence_can_be_approved(self):
        self.artifacts["tests.v1"].update(outcomes=["passed", "passed"], exit_code=0)
        self.runtime = make_runtime(artifacts=self.artifacts)
        self.assertTrue(self.runtime.submit(self.changed(self.report, passed=2, failed=0, status="passed")).accepted)
        self.assertTrue(self.runtime.submit(self.review).accepted)

    def test_unannotated_protocol_keeps_structural_behavior(self):
        protocol = json.loads((ROOT / "protocol.json").read_text())
        for transition in protocol["transitions"]:
            transition.pop("contract")
        runtime = make_runtime(protocol=protocol)
        self.assertTrue(runtime.submit(self.report).accepted)
        self.assertTrue(runtime.submit(self.review).accepted)

    def test_validator_exception_fails_closed(self):
        def broken(p, ctx):
            raise RuntimeError("plugin crash")
        self.runtime = make_runtime(checks={**CHECKS, "test_schema": broken})
        self.rejection(self.report, "test_schema")

    def test_plugin_mutation_does_not_change_committed_data(self):
        def mutate(p, ctx):
            p["failed"] = 0
            ctx["artifacts"].clear()
            ctx["history"].clear()
            return []
        self.runtime = make_runtime(checks={**CHECKS, "test_schema": mutate})
        self.assertTrue(self.runtime.submit(self.report).accepted)
        self.assertEqual(self.runtime.history[0].payload["failed"], 1)
        self.assertEqual(self.runtime.artifacts, self.artifacts)

    def test_external_mutation_cannot_rewrite_history(self):
        self.runtime.submit(self.report)
        self.report.payload["failed"] = 0
        history = self.runtime.history
        history[0].payload["failed"] = 0
        artifacts = self.runtime.artifacts
        artifacts.clear()
        audit = self.runtime.audit
        audit.clear()
        self.assertEqual(self.runtime.history[0].payload["failed"], 1)
        self.assertEqual(self.runtime.artifacts, self.artifacts)
        self.assertEqual(len(self.runtime.audit), 1)

    def test_concurrent_submission_commits_only_once(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            decisions = list(pool.map(self.runtime.submit, [self.report, self.report]))
        self.assertEqual(sum(d.accepted for d in decisions), 1)
        self.assertEqual(len(self.runtime.history), 1)
        self.assertEqual(self.runtime.state, "await_review")

    def test_unknown_check_and_contract_fail_at_startup(self):
        protocol = json.loads((ROOT / "protocol.json").read_text())
        contracts = json.loads((ROOT / "contracts.json").read_text())
        with self.assertRaises(ValueError):
            Runtime(protocol, contracts, {}, self.artifacts)
        protocol["transitions"][0]["contract"] = "unknown.v1"
        with self.assertRaises(ValueError):
            Runtime(protocol, contracts, CHECKS, self.artifacts)

    def test_demo_covers_all_four_scenarios(self):
        scenarios = run_demo()["scenarios"]
        self.assertTrue(scenarios[0]["false_approval"]["accepted"])
        self.assertFalse(scenarios[1]["false_approval"]["accepted"])
        self.assertTrue(scenarios[1]["repaired_review"]["accepted"])
        self.assertFalse(scenarios[2]["decision"]["accepted"])
        self.assertFalse(scenarios[3]["decision"]["accepted"])


if __name__ == "__main__":
    unittest.main()
