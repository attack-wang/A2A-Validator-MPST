"""Offline checks for the optional ChatDev 1.0 phase-local MPST pilot."""

from types import SimpleNamespace
from unittest.mock import Mock
from pathlib import Path
from tempfile import TemporaryDirectory
import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "ollama")

from chatdev.mpst_pilot import PhaseExchangeMonitor, run_checked_exchange
from chatdev.mpst_global import GlobalPilotMonitor
from chatdev.phase import Coding
from chatdev.chat_env import ChatEnv
from camel.typing import ModelType


class PhaseExchangeTests(unittest.TestCase):
    def test_valid_exchange_and_wrong_order(self):
        monitor = PhaseExchangeMonitor()
        with self.assertRaises(RuntimeError):
            monitor.response(SimpleNamespace(content="too early"))
        monitor.request(SimpleNamespace(content="request"))
        monitor.response(SimpleNamespace(content="response"))
        self.assertTrue(monitor.complete)

    def test_empty_response_rolls_back_and_retries(self):
        responses = iter(("", "working code"))
        seen_messages = []
        retries = []

        def generate(message):
            seen_messages.append(message.content)
            return SimpleNamespace(msg=SimpleNamespace(content=next(responses))), None

        answer, _, retry_count = run_checked_exchange(
            SimpleNamespace(content="original request"),
            generate,
            lambda _message, attempt: SimpleNamespace(content=f"retry {attempt}"),
            2,
            "Coding",
            retries.append,
        )
        self.assertEqual(answer.msg.content, "working code")
        self.assertEqual(retry_count, 1)
        self.assertEqual(seen_messages, ["original request", "retry 1"])
        self.assertEqual(retries, [1])

    def test_retry_limit(self):
        calls = []

        def generate(message):
            calls.append(message.content)
            return SimpleNamespace(msg=SimpleNamespace(content="")), None

        with self.assertRaisesRegex(RuntimeError, "after 2 retries"):
            run_checked_exchange(
                SimpleNamespace(content="request"),
                generate,
                lambda _message, attempt: SimpleNamespace(content=f"retry {attempt}"),
                2,
                "Coding",
            )
        self.assertEqual(len(calls), 3)


class GlobalProtocolTests(unittest.TestCase):
    def test_optional_phases_can_be_skipped(self):
        monitor = GlobalPilotMonitor()
        for phase in (
            "DemandAnalysis", "LanguageChoose", "Coding", "CodeReviewComment",
            "CodeReviewModification",
        ):
            monitor.begin_phase(phase, "request")
            monitor.end_phase(phase, "response")
        monitor.finish()
        self.assertEqual(monitor.checked_phases, 5)

    def test_completion_review_and_test_path(self):
        monitor = GlobalPilotMonitor()
        for phase in (
            "DemandAnalysis", "LanguageChoose", "Coding", "CodeComplete",
            "CodeComplete", "CodeReviewComment", "CodeReviewModification",
            "TestErrorSummary", "TestModification",
        ):
            monitor.begin_phase(phase, "request", {"test_reports": "traceback"})
            monitor.end_phase(phase, "response")
        monitor.finish()
        self.assertEqual(monitor.checked_phases, 9)

    def test_test_path_without_review_fix_is_rejected(self):
        monitor = GlobalPilotMonitor()
        for phase in (
            "DemandAnalysis", "LanguageChoose", "Coding", "CodeReviewComment",
        ):
            monitor.begin_phase(phase, "request", {"test_reports": "traceback"})
            monitor.end_phase(phase, "response")
        with self.assertRaisesRegex(RuntimeError, "Global MPST rejected"):
            monitor.begin_phase(
                "TestErrorSummary", "request", {"test_reports": "traceback"}
            )

    def test_dependency_repair_can_skip_test_summary_exchange(self):
        monitor = GlobalPilotMonitor()
        for phase in (
            "DemandAnalysis", "LanguageChoose", "Coding", "CodeReviewComment",
            "CodeReviewModification", "TestModification",
        ):
            monitor.begin_phase(phase, "request", {"test_reports": "ModuleNotFoundError"})
            monitor.end_phase(phase, "response")
        monitor.finish()
        self.assertEqual(monitor.checked_phases, 6)

    def test_wrong_phase_order_is_rejected(self):
        monitor = GlobalPilotMonitor()
        with self.assertRaisesRegex(RuntimeError, "Global MPST rejected"):
            monitor.begin_phase("Coding", "request")

    def test_cannot_regress_to_completion_after_review(self):
        monitor = GlobalPilotMonitor()
        for phase in ("DemandAnalysis", "LanguageChoose", "Coding", "CodeReviewComment"):
            monitor.begin_phase(phase, "request")
            monitor.end_phase(phase, "response")
        with self.assertRaisesRegex(RuntimeError, "Global MPST rejected"):
            monitor.begin_phase("CodeComplete", "late completion")

    def test_unparseable_coding_result_rolls_back_and_retries(self):
        monitor = SimpleNamespace(snapshot=Mock(return_value="before-coding"), restore=Mock())
        env = SimpleNamespace(env_dict={"task_prompt": "make a program"}, memory=None,
                              global_mpst_monitor=monitor)
        prompts = {
            role: "role prompt" for role in (
                "Programmer", "Chief Technology Officer", "Chief Executive Officer", "Counselor"
            )
        }
        phase = Coding(
            assistant_role_name="Programmer",
            user_role_name="Chief Technology Officer",
            phase_prompt="Write code",
            role_prompts=prompts,
            phase_name="Coding",
            model_type=ModelType.GPT_4O,
            log_filepath="unused.log",
        )
        phase.update_phase_env = Mock()
        phase.chatting = Mock(side_effect=["only analysis", "main.py\n```python\npass\n```"])
        phase.update_chat_env = Mock(side_effect=[ValueError("No Valid Codes."), env])
        with unittest.mock.patch.dict(os.environ, {"CHATDEV_MPST_MAX_RETRIES": "2"}):
            result = phase.execute(env, 1, False)
        self.assertIs(result, env)
        self.assertEqual(phase.chatting.call_count, 2)
        self.assertIn("skip analysis", phase.chatting.call_args.kwargs["phase_prompt"])
        monitor.restore.assert_called_once_with("before-coding")

    def test_generated_program_uses_the_same_python_runtime(self):
        with TemporaryDirectory() as directory:
            Path(directory, "main.py").write_text(
                "import sys\nprint(sys.version_info.major, sys.version_info.minor)\n",
                encoding="utf-8",
            )
            fake_env = SimpleNamespace(env_dict={"directory": directory})
            has_bugs, report = ChatEnv.exist_bugs(fake_env)
            self.assertFalse(has_bugs, report)


if __name__ == "__main__":
    unittest.main()
