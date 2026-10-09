"""Offline integration tests: real ChatDev phases/projection, stubbed model only."""
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
CHATDEV = ROOT / "integrations" / "ChatDev1.0"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(CHATDEV))
os.environ.setdefault("OPENAI_API_KEY", "offline-test")
os.environ["CHATDEV_CONTENT_ENABLED"] = "true"
os.environ["MPST_A2A_ROOT"] = str(ROOT)

from content_lab.chatdev_contracts import ChatDevContracts, ContentViolation, snapshot, smoke_run, startup_evidence
from camel.agents.role_playing import RolePlaying
from camel.agents.chat_agent import ChatAgentResponse
from camel.messages import ChatMessage
from camel.typing import RoleType, ModelType
from chatdev.chat_env import ChatEnv, ChatEnvConfig
from chatdev.content_guard import ChatDevContentGuard
from chatdev.mpst_global import GlobalPilotMonitor
from chatdev.phase import (DemandAnalysis, LanguageChoose, Coding, CodeReviewComment,
                           CodeReviewModification, TestErrorSummary, TestModification)

GOOD = 'main.py\n```python\nprint("hello")\n```'
BAD = 'main.py\n```python\nprint(\n```'
BUGGY = 'main.py\n```python\nraise RuntimeError("broken")\n```'


def message(text, role="Programmer"):
    return ChatMessage(role_name=role, role_type=RoleType.ASSISTANT, meta_dict={}, role="assistant", content=text)


class ScriptedAgent:
    def __init__(self, outputs):
        self.outputs = iter(outputs)
        self.stored_messages = []
        self.info = False
        self.terminated = False
        self.role_name = "Programmer"
        self.system_message = message("system")
        self.inputs = []

    def step(self, input_message):
        self.inputs.append(input_message.content)
        self.stored_messages.append(input_message)
        text = next(self.outputs)
        if callable(text):
            text = text()
        self.info = "<INFO>" in text
        return ChatAgentResponse([message(text)], False, {})

    def update_messages(self, output):
        self.stored_messages.append(output)


def scripted_session(outputs, validator):
    session = object.__new__(RolePlaying.__wrapped__)
    session.assistant_agent = ScriptedAgent(outputs)
    session.user_agent = SimpleNamespace(step=Mock(return_value=ChatAgentResponse([message("ack")], False, {})),
                                         system_message=message("user system"), info=False, update_messages=Mock())
    session.with_critic_in_the_loop = False
    session.critic = None
    session.content_validator = validator
    session.content_max_attempts = 3
    session.init_chat = lambda *args: (None, message("original phase request"))
    return session


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.contracts = ChatDevContracts()
        self.ctx = {"files": {"main.py": 'print("hello")'}, "phase_env": {}, "phase": "Coding",
                    "last_review": None, "evidence": None}

    def validate(self, phase, text):
        self.ctx["phase"] = phase
        self.contracts.validate(phase, text, self.ctx)

    def test_valid_coding(self):
        self.validate("Coding", GOOD)

    def test_invalid_source_and_empty_blocks(self):
        for text in (BAD, "No code needed", ""):
            with self.subTest(text=text), self.assertRaises(ContentViolation):
                self.validate("Coding", text)

    def test_placeholder_rejected(self):
        with self.assertRaisesRegex(ContentViolation, "unimplemented_function"):
            self.validate("Coding", 'main.py\n```python\ndef solve():\n    pass\n```')

    def test_completion_must_return_requested_file(self):
        self.ctx["files"]["helper.py"] = "def solve():\n    pass"
        self.ctx["phase_env"]["unimplemented_file"] = "helper.py"
        with self.assertRaisesRegex(ContentViolation, "requested_file"):
            self.validate("CodeComplete", GOOD)

    def test_review_before_tests_does_not_require_test_report(self):
        self.validate("CodeReviewComment", '{"verdict":"finished","issues":[]}')

    def test_review_requires_actual_source_location(self):
        for issue in ({"file": "invented.py", "line": 1, "message": "fix"},
                      {"file": "main.py", "line": 999, "message": "fix"}):
            with self.assertRaisesRegex(ContentViolation, "issue_location"):
                self.validate("CodeReviewComment", json.dumps({"verdict": "changes_requested", "issues": [issue]}))

    def test_review_verdict_and_issues_agree(self):
        with self.assertRaisesRegex(ContentViolation, "review_verdict"):
            self.validate("CodeReviewComment", '{"verdict":"changes_requested","issues":[]}')

    def test_review_finished_cannot_ignore_compile_error(self):
        self.ctx["files"] = {"main.py": "print("}
        with self.assertRaisesRegex(ContentViolation, "python_compile"):
            self.validate("CodeReviewComment", '{"verdict":"finished","issues":[]}')

    def test_review_fix_finished_requires_finished_review(self):
        self.ctx["last_review"] = {"verdict": "changes_requested"}
        with self.assertRaisesRegex(ContentViolation, "premature_finished"):
            self.validate("CodeReviewModification", "<INFO> Finished")

    def test_language_contract_matches_python_profile(self):
        self.validate("LanguageChoose", "Python")
        with self.assertRaisesRegex(ContentViolation, "python_profile"):
            self.validate("LanguageChoose", "JavaScript")

    def test_test_summary_matches_trusted_evidence(self):
        self.ctx["evidence"] = {"id": "run-1", "snapshot_id": snapshot(self.ctx["files"])["id"], "status": "failed"}
        self.validate("TestErrorSummary", '{"status":"failed","test_run_id":"run-1","summary":"startup raised"}')
        with self.assertRaisesRegex(ContentViolation, "summary_evidence"):
            self.validate("TestErrorSummary", '{"status":"passed","test_run_id":"run-1","summary":"all passed"}')

    def test_stale_execution_evidence_cannot_support_summary(self):
        self.ctx["evidence"] = {"id": "old", "snapshot_id": "old-source", "status": "passed"}
        with self.assertRaisesRegex(ContentViolation, "test_snapshot"):
            self.validate("TestErrorSummary", '{"status":"passed","test_run_id":"old","summary":"ok"}')

    def test_failing_test_cannot_be_skipped(self):
        self.ctx["evidence"] = {"status": "failed"}
        with self.assertRaisesRegex(ContentViolation, "premature_finished"):
            self.validate("TestModification", "<INFO> Finished")

    def test_real_smoke_exit_status_and_version(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "main.py"
            path.write_text("print('ok')", encoding="utf-8")
            evidence = smoke_run(directory, {"main.py": "print('ok')"})
            self.assertEqual(evidence["status"], "passed")
            self.assertEqual(evidence["exit_code"], 0)
            evidence = smoke_run(directory, {"main.py": "changed source"})
            self.assertEqual(evidence["status"], "inconclusive")
            path.write_text("raise RuntimeError('fail')", encoding="utf-8")
            evidence = smoke_run(directory, {"main.py": "raise RuntimeError('fail')"})
            self.assertEqual(evidence["status"], "failed")

    def test_timeout_is_inconclusive_not_passed(self):
        with TemporaryDirectory() as directory:
            code = "import time\ntime.sleep(2)"
            (Path(directory) / "main.py").write_text(code, encoding="utf-8")
            self.assertEqual(smoke_run(directory, {"main.py": code}, timeout=0.1)["status"], "inconclusive")

    def test_multifile_chatdev_source_can_import_local_modules(self):
        files = {"main.py": "from helper import value\nprint(value)", "helper.py": "value = 42"}
        with TemporaryDirectory() as directory:
            for name, body in files.items():
                (Path(directory) / name).write_text(body, encoding="utf-8")
            evidence = smoke_run(directory, files)
            self.assertEqual(evidence["status"], "passed")
            self.assertEqual(evidence["stdout"].strip(), "42")

    def test_source_changed_during_startup_invalidates_evidence(self):
        files = {"main.py": "from pathlib import Path\nPath('main.py').write_text('print(42)', encoding='utf-8')"}
        with TemporaryDirectory() as directory:
            (Path(directory) / "main.py").write_text(files["main.py"], encoding="utf-8")
            self.assertEqual(smoke_run(directory, files)["status"], "inconclusive")

    def test_host_report_contract_rejects_changed_execution_record(self):
        files = {"main.py": "print(42)"}
        with TemporaryDirectory() as directory:
            (Path(directory) / "main.py").write_text(files["main.py"], encoding="utf-8")
            evidence = smoke_run(directory, files)
            self.assertEqual(startup_evidence(evidence, files), [])
            evidence["stdout"] = "invented output"
            self.assertEqual(startup_evidence(evidence, files)[0].rule, "startup_record_digest")

    def test_roleplaying_rejects_before_delivery_and_retries(self):
        session = scripted_session([BAD, GOOD], lambda text: self.validate("Coding", text))
        response, _ = session.step(message("request"), assistant_only=False)
        self.assertEqual(response.msg.content, GOOD)
        self.assertEqual(len(session.assistant_agent.inputs), 2)
        self.assertIn("python_compile", session.assistant_agent.inputs[1])
        # Only the accepted output reached the other agent.
        session.user_agent.step.assert_called_once()
        self.assertEqual(session.user_agent.step.call_args.args[0].content, GOOD)
        self.assertFalse(any(m.content == BAD for m in session.assistant_agent.stored_messages))

    def test_roleplaying_exhaustion_delivers_nothing(self):
        session = scripted_session([BAD, BAD, BAD], lambda text: self.validate("Coding", text))
        with self.assertRaises(ContentViolation):
            session.step(message("request"), assistant_only=False)
        session.user_agent.step.assert_not_called()
        self.assertEqual(session.assistant_agent.stored_messages, [])


class PhaseIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = ChatEnv(ChatEnvConfig(False, False, False, False, "offline", False))
        self.env.env_dict.update(directory=self.temp.name, task_prompt="Print hello", task_description="")
        self.env.codes.directory = self.temp.name
        self.env.content_guard = ChatDevContentGuard(GlobalPilotMonitor(), self.env)
        self.guard = self.env.content_guard
        self.env.global_mpst_monitor = self.guard.monitor
        self.phase_config = json.loads((CHATDEV / "CompanyConfig/Default/PhaseConfig.json").read_text(encoding="utf-8"))
        roles = json.loads((CHATDEV / "CompanyConfig/Default/RoleConfig.json").read_text(encoding="utf-8"))
        self.roles = {name: "\n".join(text) for name, text in roles.items()}
        for role in roles:
            self.env.recruit(role)
        self.log = Path(self.temp.name) / "run.log"
        self.log.write_text("", encoding="utf-8")
        self.silence = patch("chatdev.phase.log_visualize")
        self.silence.start()
        self.addCleanup(self.silence.stop)
        for name in ("chatdev.codes.log_visualize", "chatdev.phase.get_info", "chatdev.utils.log_visualize"):
            patcher = patch(name, return_value="offline statistics")
            patcher.start()
            self.addCleanup(patcher.stop)

    def phase(self, kind):
        name = kind.__name__
        config = self.phase_config[name]
        phase = kind(assistant_role_name=config["assistant_role_name"], user_role_name=config["user_role_name"],
                     phase_prompt="\n".join(config["phase_prompt"]), role_prompts=self.roles,
                     phase_name=name, model_type=ModelType.STUB, log_filepath=str(self.log))
        phase.phase_env.update(cycle_index=1, cycle_num=1)
        return phase

    def run_phase(self, kind, result):
        phase = self.phase(kind)
        phase.chatting = Mock(return_value=result)
        phase.execute(self.env, 1, False)
        return phase

    def prefix(self, code=GOOD):
        self.run_phase(DemandAnalysis, "application")
        self.run_phase(LanguageChoose, "Python")
        self.run_phase(Coding, code)

    def reviewed(self, code=GOOD):
        self.prefix(code)
        self.run_phase(CodeReviewComment, '{"verdict":"finished","issues":[]}')
        self.run_phase(CodeReviewModification, "<INFO> Finished")

    def summary(self, expected="passed"):
        phase = self.phase(TestErrorSummary)
        def output(**kwargs):
            evidence = self.guard.evidence
            return json.dumps({"status": expected, "test_run_id": evidence["id"], "summary": "startup result"})
        phase.chatting = Mock(side_effect=output)
        phase.execute(self.env, 1, False)

    def test_actual_projection_uses_isolated_sources(self):
        import gt_projection, mpst_validator
        self.assertTrue(Path(gt_projection.__file__).is_relative_to(ROOT))
        self.assertTrue(Path(mpst_validator.__file__).is_relative_to(ROOT))

    def test_real_init_chat_preserves_json_literals_in_contract_prompt(self):
        session = scripted_session([GOOD], None)
        session.assistant_agent.reset = Mock()
        session.assistant_agent.use_memory = Mock(return_value=None)
        session.user_agent.reset = Mock()
        session.user_agent.role_name = "Reviewer"
        session.user_sys_msg = message("user system", role="Reviewer")
        for kind in (CodeReviewComment, TestErrorSummary):
            phase = self.phase(kind)
            self.guard.evidence = {"id": "host-record", "status": "passed", "stdout": "{nested braces}"}
            placeholders = {name: "context" for name in ("task", "modality", "language", "ideas", "codes", "test_reports")}
            with patch("camel.agents.role_playing.log_visualize"):
                _, request = RolePlaying.__wrapped__.init_chat(session, None, placeholders, self.guard.prompt_for(phase))
            if kind is CodeReviewComment:
                self.assertIn('"verdict"', request.content)
            else:
                self.assertIn('"host-record"', request.content)
                self.assertIn('{nested braces}', request.content)

    def test_content_failure_does_not_apply_source_or_advance_mpst(self):
        self.run_phase(DemandAnalysis, "application")
        self.run_phase(LanguageChoose, "Python")
        expected = self.guard.monitor.monitor.expected_transitions("Coordinator")
        with self.assertRaises(ContentViolation):
            self.run_phase(Coding, BAD)
        self.assertEqual(self.guard.monitor.monitor.expected_transitions("Coordinator"), expected)
        self.assertEqual(self.env.codes.codebooks, {})
        self.assertFalse((Path(self.temp.name) / "main.py").exists())
        self.assertEqual(self.guard.monitor.checked_phases, 2)

    def test_wrong_phase_order_rejected_before_generation(self):
        phase = self.phase(Coding)
        phase.chatting = Mock(return_value=GOOD)
        with self.assertRaisesRegex(RuntimeError, "Global MPST rejected"):
            phase.execute(self.env, 1, False)
        phase.chatting.assert_not_called()

    def test_good_workflow_and_real_final_acceptance(self):
        self.reviewed()
        self.summary()
        self.guard.finish()
        self.assertTrue(self.guard.monitor.monitor.validators["Coordinator"].protocol.is_complete())
        audit = json.loads((Path(self.temp.name) / "content-contract-audit.json").read_text(encoding="utf-8"))
        self.assertTrue(audit["checks"][-1]["accepted"])
        self.assertEqual(audit["checks"][-1]["contract"], "chatdev.stage_exit.v1")

    def test_actual_test_summary_cannot_forge_pass(self):
        self.reviewed(BUGGY)
        expected = self.guard.monitor.monitor.expected_transitions("Coordinator")
        with self.assertRaisesRegex(ContentViolation, "summary_evidence"):
            self.summary("passed")
        self.assertEqual(self.guard.monitor.monitor.expected_transitions("Coordinator"), expected)

    def test_fix_changes_snapshot_and_requires_new_execution(self):
        self.reviewed(BUGGY)
        self.summary("failed")
        old = self.guard.evidence["snapshot_id"]
        self.run_phase(TestModification, GOOD)
        self.guard.finish()
        self.assertNotEqual(self.guard.evidence["snapshot_id"], old)
        self.assertEqual(self.guard.evidence["status"], "passed")

    def test_unfixed_startup_failure_cannot_finish(self):
        self.reviewed(BUGGY)
        self.summary("failed")
        self.run_phase(TestModification, BUGGY)
        expected = self.guard.monitor.monitor.expected_transitions("Coordinator")
        with self.assertRaisesRegex(ContentViolation, "current_startup_passed"):
            self.guard.finish()
        self.assertEqual(self.guard.monitor.monitor.expected_transitions("Coordinator"), expected)

    def test_actual_chatting_uses_roleplaying_content_hook(self):
        self.run_phase(DemandAnalysis, "application")
        self.run_phase(LanguageChoose, "Python")
        phase = self.phase(Coding)
        session = scripted_session([BAD, GOOD], None)
        with patch("chatdev.phase.RolePlaying", return_value=session):
            phase.execute(self.env, 1, False)
        self.assertEqual(len(session.assistant_agent.inputs), 2)
        self.assertEqual((Path(self.temp.name) / "main.py").read_text(encoding="utf-8"), 'print("hello")')
        self.assertEqual(self.guard.monitor.checked_phases, 3)

    def test_apply_io_failure_restores_source_buffers_disk_and_protocol(self):
        self.run_phase(DemandAnalysis, "application")
        self.run_phase(LanguageChoose, "Python")
        expected = self.guard.monitor.monitor.expected_transitions("Coordinator")
        phase = self.phase(Coding)
        phase.chatting = Mock(return_value=GOOD)
        def broken_apply(env):
            env.codes.codebooks["main.py"] = 'print("partially written")'
            (Path(self.temp.name) / "main.py").write_text('print("partially written")')
            raise OSError("write failed")
        phase.update_chat_env = broken_apply
        with self.assertRaises(OSError):
            phase.execute(self.env, 1, False)
        self.assertEqual(self.env.codes.codebooks, {})
        self.assertFalse((Path(self.temp.name) / "main.py").exists())
        self.assertEqual(self.guard.monitor.monitor.expected_transitions("Coordinator"), expected)

    def test_full_chat_chain_config_with_real_phase_hooks(self):
        from chatdev.chat_chain import ChatChain
        config = CHATDEV / "CompanyConfig/MPSTContent"
        with patch.object(ChatChain, "get_logfilepath", return_value=("offline", str(self.log))):
            chain = ChatChain(config_path=str(config / "ChatChainConfig.json"),
                              config_phase_path=str(config / "PhaseConfig.json"),
                              config_role_path=str(config / "RoleConfig.json"),
                              task_prompt="Print hello", project_name="Offline", org_name="Content", model_type=ModelType.STUB)
        chain.chat_env.env_dict.update(directory=self.temp.name, task_prompt="Print hello")
        chain.chat_env.codes.directory = self.temp.name
        for role in chain.role_prompts:
            chain.chat_env.recruit(role)
        def summary():
            evidence = chain.chat_env.content_guard.evidence
            return json.dumps({"status": evidence["status"], "test_run_id": evidence["id"], "summary": "startup evidence"})
        plans = iter((["application"], ["Python"], [BAD, GOOD],
                      ['{"verdict":"finished","issues":[]}'], ["<INFO> Finished"], [summary]))
        sessions = []
        def factory(**kwargs):
            session = scripted_session(next(plans), None)
            sessions.append(session)
            return session
        with patch("chatdev.phase.RolePlaying", side_effect=factory), patch("chatdev.composed_phase.log_visualize"), patch("chatdev.chat_chain.log_visualize"):
            chain.execute_chain()
        guard = chain.chat_env.content_guard
        self.assertEqual(guard.monitor.checked_phases, 6)
        self.assertEqual(len(sessions[2].assistant_agent.inputs), 2)
        self.assertTrue(guard.monitor.monitor.validators["Coordinator"].protocol.is_complete())
        result = {"model_mode": "scripted_offline", "protocol_engine": "copied_actual_mpst_projection",
                  "checked_phases": guard.monitor.checked_phases, "coding_attempts": len(sessions[2].assistant_agent.inputs),
                  "terminal": True, "delivered": guard.delivered, "audit": guard.contracts.audit}
        destination = ROOT / "output" / "chatdev-offline-integration.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
