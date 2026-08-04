"""Behavior tests for the shared MPST runtime core."""

from __future__ import annotations

import json
import asyncio
import os
import sys
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "mpst-runtime" / "mpst_ext"))
sys.path.insert(
    0,
    str(
        ROOT
        / "host-platform"
        / "backend"
        / "python"
        / "hosts"
        / "multiagent"
    ),
)

from a2a.types import Message, Part, Role, TextPart  # noqa: E402
from host_mpst_monitor import HostProtocolMonitor  # noqa: E402
from mpst_ext import (  # noqa: E402
    MPSTValidatingExecutor,
    resolve_validation_enabled,
)
from mpst_ext.mpst_validator import MPSTValidator, ValidatorRegistry  # noqa: E402


class MPSTValidatorTests(unittest.TestCase):
    def test_validation_switch_defaults_on_and_parses_false(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(resolve_validation_enabled())
        with patch.dict(
            os.environ,
            {"VALIDATION_ENABLED": "false"},
            clear=True,
        ):
            self.assertFalse(resolve_validation_enabled())
        with patch.dict(
            os.environ,
            {"VALIDATION_ENABLED": "invalid"},
            clear=True,
        ):
            with self.assertRaises(ValueError):
                resolve_validation_enabled()

    def test_linear_protocol_blocks_wrong_label_and_finishes(self):
        validator = MPSTValidator()
        self.assertTrue(
            validator.set_protocol(
                "Host?request__str.Host!response__str.0",
                "Agent",
            )
        )
        self.assertTrue(
            validator.validate_message(
                "[request: hello]", "receive", sender="Host"
            )["is_valid"]
        )
        violation = validator.validate_message(
            "[wrong: hello]", "send", receiver="Host"
        )
        self.assertFalse(violation["is_valid"])
        self.assertEqual("WrongLabel", violation["code"])
        self.assertTrue(
            validator.validate_message(
                "[response: ok]", "send", receiver="Host"
            )["is_valid"]
        )
        self.assertTrue(validator.finalize()["is_valid"])

    def test_choice_matches_actual_peer(self):
        validator = MPSTValidator()
        self.assertTrue(
            validator.set_protocol(
                "(Train!book__str.Train?ticket__str.0 + "
                "Flight!book__str.Flight?ticket__str.0)",
                "Host",
            )
        )
        self.assertEqual(2, len(validator.get_status()["expected_transitions"]))
        self.assertTrue(
            validator.validate_message(
                "[book: trip]", "send", receiver="Flight"
            )["is_valid"]
        )
        self.assertTrue(
            validator.validate_message(
                "[ticket: F100]", "receive", sender="Flight"
            )["is_valid"]
        )
        self.assertTrue(validator.finalize()["is_valid"])

    def test_host_monitor_infers_choice_label_from_selected_peer(self):
        monitor = HostProtocolMonitor()
        self.assertTrue(
            monitor.load_from_local_protocol(
                "(Train!booktrain__str.Train?trainticket__str.0 + "
                "Flight!bookflight__str.Flight?flightticket__str.0)",
                "Travel",
            )
        )

        result, wrapped = monitor.prepare_outgoing(
            "train-session",
            peer="Train",
            content="南京至北京，2位成人",
        )

        self.assertTrue(result["is_valid"])
        self.assertEqual(
            "[booktrain: 南京至北京，2位成人]",
            wrapped,
        )
        self.assertTrue(
            monitor.validate_incoming(
                "train-session",
                peer="Train",
                content="[trainticket: G12]",
            )["is_valid"]
        )
        self.assertTrue(monitor.finalize("train-session")["is_valid"])

    def test_recursive_cycle_is_a_completion_boundary(self):
        validator = MPSTValidator()
        self.assertTrue(
            validator.set_protocol(
                "mu t.Host?number__float.Host!result__float.t",
                "OP1",
            )
        )
        self.assertTrue(
            validator.validate_message(
                "[number: 2]", "receive", sender="Host"
            )["is_valid"]
        )
        self.assertTrue(
            validator.validate_message(
                "[result: 4]", "send", receiver="Host"
            )["is_valid"]
        )
        self.assertTrue(validator.finalize()["is_valid"])

    def test_session_state_is_isolated(self):
        registry = ValidatorRegistry("Agent")
        self.assertTrue(
            registry.register_protocol(
                "test",
                "Host?request__str.Host!response__str.0",
            )
        )
        first = registry.get("session-a")
        second = registry.get("session-b")
        self.assertTrue(
            first.validate_message(
                "[request: A]", "receive", sender="Host"
            )["is_valid"]
        )
        self.assertNotEqual(
            first.get_status()["current_position"],
            second.get_status()["current_position"],
        )

    def test_tool_call_leak_is_retryable_and_does_not_advance_state(self):
        validator = MPSTValidator()
        self.assertTrue(
            validator.set_protocol(
                "Host?request__str.Host!response__str.0",
                "Agent",
            )
        )
        self.assertTrue(
            validator.validate_message(
                "[request: hello]", "receive", sender="Host"
            )["is_valid"]
        )
        position_before = validator.get_status()["current_position"]

        leaked = validator.validate_message(
            {
                "name": "lookup_value",
                "arguments": {"key": "hello"},
            },
            "send",
            receiver="Host",
            generation_metadata={
                "tool_required": True,
                "tool_call_observed": True,
                "tool_response_observed": False,
                "unexecuted_tool_call": True,
                "tool_name": "lookup_value",
            },
        )

        self.assertFalse(leaked["is_valid"])
        self.assertTrue(leaked["retryable"])
        self.assertEqual("ToolCallIncomplete", leaked["code"])
        self.assertEqual(
            position_before,
            validator.get_status()["current_position"],
        )

    def test_executor_retries_incomplete_tool_call_in_same_session(self):
        class FakeAgent:
            requires_tool_call = True

            def __init__(self):
                self.prompts = []

            async def stream(self, prompt, _session_id):
                self.prompts.append(prompt)
                if len(self.prompts) == 1:
                    yield {
                        "is_task_complete": True,
                        "content": (
                            '{"name":"lookup_value",'
                            '"arguments":{"key":"hello"}}'
                        ),
                        "tool_required": True,
                        "tool_call_observed": True,
                        "tool_response_observed": False,
                        "unexecuted_tool_call": True,
                        "tool_name": "lookup_value",
                    }
                    return
                yield {
                    "is_task_complete": True,
                    "content": "[response: recovered]",
                    "tool_required": True,
                    "tool_call_observed": True,
                    "tool_response_observed": True,
                    "unexecuted_tool_call": False,
                    "tool_name": "lookup_value",
                }

        class FakeUpdater:
            def __init__(self):
                self.statuses = []
                self.artifacts = []
                self.completed = False

            def new_agent_message(self, parts):
                return parts

            async def update_status(self, *args, **kwargs):
                self.statuses.append((args, kwargs))

            async def add_artifact(self, *args, **kwargs):
                self.artifacts.append((args, kwargs))

            async def complete(self):
                self.completed = True

        async def run_case():
            executor = MPSTValidatingExecutor("Agent")
            executor.agent = FakeAgent()
            self.assertTrue(
                executor._validation_ext.set_protocol(
                    "Host?request__str.Host!response__str.0",
                    "ToolRecovery",
                )
            )
            message = Message(
                role=Role.user,
                parts=[Part(root=TextPart(text="[request: hello]"))],
                message_id=str(uuid.uuid4()),
                context_id="tool-retry-session",
            )
            context = SimpleNamespace(message=message)
            task = SimpleNamespace(id="task", context_id="tool-retry-session")
            updater = FakeUpdater()

            await executor._execute_with_validation(context, task, updater)

            self.assertEqual(2, len(executor.agent.prompts))
            self.assertIn("Regenerate the tool call", executor.agent.prompts[1])
            self.assertTrue(updater.completed)
            self.assertEqual(1, len(updater.artifacts))
            status = executor._validation_ext.get_status("tool-retry-session")
            self.assertTrue(status["complete"])
            self.assertEqual(2, len(status["position_history"]))
            self.assertEqual(
                "ToolCallIncomplete",
                status["violations"][0]["code"],
            )

        asyncio.run(run_case())

    def test_executor_fails_closed_after_tool_retry_limit(self):
        class AlwaysBrokenAgent:
            requires_tool_call = True

            def __init__(self):
                self.calls = 0

            async def stream(self, _prompt, _session_id):
                self.calls += 1
                yield {
                    "is_task_complete": True,
                    "content": "Error: Tool call not executed - lookup_value",
                    "tool_required": True,
                    "tool_call_observed": True,
                    "tool_response_observed": False,
                    "unexecuted_tool_call": True,
                    "tool_name": "lookup_value",
                }

        class FakeUpdater:
            def __init__(self):
                self.statuses = []
                self.artifact_published = False
                self.completed = False

            def new_agent_message(self, parts):
                return parts

            async def update_status(self, *args, **kwargs):
                self.statuses.append((args, kwargs))

            async def add_artifact(self, *_args, **_kwargs):
                self.artifact_published = True

            async def complete(self):
                self.completed = True

        async def run_case():
            executor = MPSTValidatingExecutor(
                "Agent",
                max_tool_call_retries=2,
            )
            executor.agent = AlwaysBrokenAgent()
            self.assertTrue(
                executor._validation_ext.set_protocol(
                    "Host?request__str.Host!response__str.0",
                    "ToolRetryLimit",
                )
            )
            message = Message(
                role=Role.user,
                parts=[Part(root=TextPart(text="[request: hello]"))],
                message_id=str(uuid.uuid4()),
                context_id="tool-retry-limit-session",
            )
            context = SimpleNamespace(message=message)
            task = SimpleNamespace(
                id="task",
                context_id="tool-retry-limit-session",
            )
            updater = FakeUpdater()

            await executor._execute_with_validation(context, task, updater)

            self.assertEqual(3, executor.agent.calls)
            self.assertFalse(updater.artifact_published)
            self.assertFalse(updater.completed)
            status = executor._validation_ext.get_status(
                "tool-retry-limit-session"
            )
            self.assertFalse(status["complete"])
            self.assertEqual(1, len(status["position_history"]))
            self.assertEqual(3, len(status["violations"]))

        asyncio.run(run_case())

    def test_disabled_executor_passes_tool_call_through_without_protocol(self):
        leaked_tool_call = (
            'Tool Calls: [{"type":"function","function":'
            '{"name":"lookup_value","arguments":{"key":"hello"}}}]'
        )

        class BaselineAgent:
            def __init__(self):
                self.calls = 0

            async def stream(self, _prompt, _session_id):
                self.calls += 1
                yield {
                    "is_task_complete": True,
                    "content": leaked_tool_call,
                    "unexecuted_tool_call": True,
                }

        class FakeUpdater:
            def __init__(self):
                self.artifacts = []
                self.completed = False

            async def update_status(self, *_args, **_kwargs):
                return None

            async def add_artifact(self, *args, **kwargs):
                self.artifacts.append((args, kwargs))

            async def complete(self):
                self.completed = True

        async def run_case():
            executor = MPSTValidatingExecutor(
                "Agent",
                validation_enabled=False,
            )
            executor.agent = BaselineAgent()
            message = Message(
                role=Role.user,
                parts=[Part(root=TextPart(text="hello"))],
                message_id=str(uuid.uuid4()),
                context_id="baseline-session",
            )
            context = SimpleNamespace(message=message)
            task = SimpleNamespace(
                id="task",
                context_id="baseline-session",
            )
            updater = FakeUpdater()

            await executor._execute_without_validation(
                context,
                task,
                updater,
            )

            self.assertEqual(1, executor.agent.calls)
            self.assertTrue(updater.completed)
            self.assertEqual(1, len(updater.artifacts))
            published_parts = updater.artifacts[0][0][0]
            self.assertEqual(
                leaked_tool_call,
                published_parts[0].root.text,
            )
            self.assertFalse(executor._validation_ext.registry.has_protocol())

        asyncio.run(run_case())

    def test_travel_type_map_covers_every_message_label(self):
        protocol_path = (
            ROOT
            / "host-platform"
            / "backend"
            / "python"
            / "hosts"
            / "multiagent"
            / "protocols"
            / "Travel.gt"
        )
        type_path = protocol_path.with_suffix(".type.json")
        type_map = json.loads(type_path.read_text(encoding="utf-8"))
        protocol_text = protocol_path.read_text(encoding="utf-8")
        labels = {
            segment.split(".", 1)[0].strip()
            for segment in protocol_text.split(":")[1:]
        }
        # Remove text after a message label on lines that also contain syntax.
        labels = {label.split()[0] for label in labels if label}
        self.assertTrue(labels.issubset(type_map.keys()), labels - type_map.keys())

    def test_executor_blocks_invalid_input_before_agent_runs(self):
        class FakeAgent:
            called = False

            async def stream(self, *_args):
                self.called = True
                yield {"is_task_complete": True, "content": "should not run"}

        class FakeUpdater:
            def __init__(self):
                self.statuses = []

            def new_agent_message(self, parts):
                return parts

            async def update_status(self, *args, **kwargs):
                self.statuses.append((args, kwargs))

            async def add_artifact(self, *_args, **_kwargs):
                raise AssertionError("invalid input must not publish an artifact")

            async def complete(self):
                raise AssertionError("invalid input must not complete")

        async def run_case():
            executor = MPSTValidatingExecutor("Weatheragent")
            executor.agent = FakeAgent()
            self.assertTrue(
                executor._validation_ext.set_protocol(
                    "Host?getweather__str.Host!weatherinfo__str.0",
                    "Travel",
                )
            )
            message = Message(
                role=Role.user,
                parts=[Part(root=TextPart(text="[wrong: Beijing]"))],
                message_id=str(uuid.uuid4()),
                context_id="blocked-session",
            )
            context = SimpleNamespace(message=message)
            task = SimpleNamespace(id="task", context_id="blocked-session")
            updater = FakeUpdater()
            await executor._execute_with_validation(context, task, updater)
            self.assertFalse(executor.agent.called)
            self.assertTrue(updater.statuses)

        asyncio.run(run_case())


if __name__ == "__main__":
    unittest.main()
