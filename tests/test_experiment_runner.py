from __future__ import annotations

import json
import datetime as dt
import tempfile
import threading
import unittest

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from scripts.experiment_runner import (
    ExperimentRunner,
    event_tool_calls,
    final_output_checklist,
    load_experiment_config,
    parse_a2a_trace,
    resolve_dynamic_prompt,
)


class _FakeConversationHandler(BaseHTTPRequestHandler):
    conversations: dict[str, list[dict]] = {}
    events: list[dict] = []
    tasks: list[dict] = []
    agents: list[dict] = []
    pending_reads = 0

    def log_message(self, *_args):
        return

    def _reply(self, result):
        body = json.dumps(
            {"jsonrpc": "2.0", "id": "test", "result": result}
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length))
        method = payload["method"]
        params = payload.get("params")
        cls = type(self)

        if method == "conversation/create":
            context = f"conversation-{len(cls.conversations) + 1}"
            cls.conversations[context] = []
            self._reply(
                {
                    "conversation_id": context,
                    "is_active": True,
                    "messages": [],
                    "task_ids": [],
                }
            )
            return
        if method == "agent/register":
            cls.agents.append({"name": "Weather Agent", "url": params})
            self._reply(None)
            return
        if method == "agent/list":
            self._reply(cls.agents)
            return
        if method == "message/send":
            context = params["context_id"]
            cls.conversations[context].append(params)
            response = {
                "message_id": "response-1",
                "context_id": context,
                "role": "agent",
                "parts": [{"kind": "text", "text": "旅行计划已完成"}],
            }
            cls.conversations[context].append(response)
            cls.events.extend(
                [
                    {
                        "id": "event-user",
                        "actor": "user",
                        "timestamp": 1,
                        "content": params,
                    },
                    {
                        "id": "event-call",
                        "actor": "host_agent",
                        "timestamp": 2,
                        "content": {
                            "message_id": "call-message",
                            "context_id": context,
                            "role": "agent",
                            "parts": [
                                {
                                    "kind": "data",
                                    "data": {
                                        "name": "send_message",
                                        "args": {
                                            "agent_name": "Weather Agent",
                                            "message": "weather",
                                        },
                                    },
                                }
                            ],
                        },
                    },
                    {
                        "id": "event-response",
                        "actor": "host_agent",
                        "timestamp": 3,
                        "content": response,
                    },
                ]
            )
            cls.tasks.append(
                {
                    "id": "task-1",
                    "context_id": context,
                    "status": {"state": "completed"},
                }
            )
            cls.pending_reads = 1
            self._reply(
                {
                    "message_id": params["message_id"],
                    "context_id": context,
                }
            )
            return
        if method == "message/pending":
            if cls.pending_reads:
                cls.pending_reads -= 1
                first = next(iter(cls.conversations.values()))[0]
                self._reply([[first["message_id"], "Working..."]])
            else:
                self._reply([])
            return
        if method == "message/list":
            self._reply(cls.conversations.get(params, []))
            return
        if method == "events/get":
            self._reply(cls.events)
            return
        if method == "task/list":
            self._reply(cls.tasks)
            return
        self.send_error(404)


class ExperimentRunnerTests(unittest.TestCase):
    def setUp(self):
        _FakeConversationHandler.conversations = {}
        _FakeConversationHandler.events = []
        _FakeConversationHandler.tasks = []
        _FakeConversationHandler.agents = []
        _FakeConversationHandler.pending_reads = 0

    def test_extracts_structured_send_message_call(self):
        calls = event_tool_calls(
            [
                {
                    "id": "e1",
                    "content": {
                        "parts": [
                            {
                                "kind": "data",
                                "data": {
                                    "name": "send_message",
                                    "args": {"agent_name": "Weather Agent"},
                                },
                            }
                        ]
                    },
                }
            ]
        )
        self.assertEqual(calls[0]["name"], "send_message")
        self.assertEqual(
            calls[0]["arguments"]["agent_name"], "Weather Agent"
        )

    def test_parses_a2a_boundary_trace(self):
        trace = parse_a2a_trace(
            '2026-07-28 | INFO | host.communication | '
            '[A2A COMMUNICATION] '
            '{"direction":"outgoing","phase":"business",'
            '"peer":"Weather Agent","payload":{"kind":"message"}}'
        )
        self.assertEqual(len(trace), 1)
        self.assertEqual(trace[0]["peer"], "Weather Agent")

    def test_loads_small_config_override_from_base(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "base.json").write_text(
                json.dumps(
                    {
                        "experiment_name": "base",
                        "repetitions": 10,
                        "environment": {"A": "1", "B": "2"},
                    }
                ),
                encoding="utf-8",
            )
            child = root / "child.json"
            child.write_text(
                json.dumps(
                    {
                        "extends": "base.json",
                        "experiment_name": "large",
                        "repetitions": 100,
                        "environment": {"B": "3"},
                    }
                ),
                encoding="utf-8",
            )
            loaded = load_experiment_config(child)
            self.assertEqual("large", loaded["experiment_name"])
            self.assertEqual(100, loaded["repetitions"])
            self.assertEqual({"A": "1", "B": "3"}, loaded["environment"])

    def test_resolves_relative_travel_dates_once(self):
        resolved = resolve_dynamic_prompt(
            {
                "id": "live",
                "template": "从{start_date}至{end_date}",
                "start_offset_days": 3,
                "duration_days": 4,
            },
            dt.date(2026, 8, 30),
        )
        self.assertEqual("从2026-09-02至2026-09-05", resolved["text"])

    def test_final_output_checklist_requires_budget_agent(self):
        text = (
            "2026年8月10日去程G1，8月13日返程G2。酒店住宿3晚。"
            "故宫、颐和园、长城门票均已预约购票。雨天天气安排室内，"
            "晴天安排户外。每日乘地铁并给出换乘路线和费用。"
            "交通、酒店住宿、门票合计总费用8000元，人均4000元。"
        )
        without_budget = final_output_checklist(
            text,
            used_agents={"Train Agent", "Hotel Agent", "Ticket Agent"},
            usable=True,
        )
        with_budget = final_output_checklist(
            text,
            used_agents={
                "Train Agent",
                "Hotel Agent",
                "Ticket Agent",
                "Budget Agent",
            },
            usable=True,
        )
        self.assertEqual(5, sum(without_budget.values()))
        self.assertEqual(6, sum(with_budget.values()))

    def test_final_output_checklist_uses_dynamic_dates(self):
        text = (
            "2026-09-02去程G1，2026-09-05返程G2。酒店住宿3晚。"
            "故宫、颐和园、长城门票均已预约购票。雨天天气安排室内，"
            "晴天安排户外。每日乘地铁并给出换乘路线和费用。"
            "交通、住宿、门票合计总费用8000元，人均4000元。"
        )
        result = final_output_checklist(
            text,
            used_agents={"Budget Agent"},
            usable=True,
            expected_dates=("2026-09-02", "2026-09-05"),
        )
        self.assertEqual(6, sum(result.values()))

    def test_error_response_and_wire_failure_are_not_completed(self):
        runner = ExperimentRunner.__new__(ExperimentRunner)
        runner.config = {
            "expected_agent_groups": [["Ticket Agent"]],
            "exclusive_agent_groups": [],
        }
        summary = runner.analyze(
            run_id="failure-run",
            mode_name="validation_off",
            prompt_id="travel-standard",
            repetition=1,
            conversation="conversation-1",
            duration=12.0,
            timed_out=False,
            messages=[
                {
                    "role": "agent",
                    "parts": [
                        {
                            "kind": "text",
                            "text": (
                                "处理请求时发生错误：ValueError: "
                                "Agent Ticket Agent task failed"
                            ),
                        }
                    ],
                }
            ],
            events=[],
            tasks=[],
            log_text="",
            wire_trace=[
                {
                    "direction": "incoming",
                    "phase": "business",
                    "peer": "Ticket Agent",
                    "task_id": "task-1",
                    "payload": {
                        "id": "task-1",
                        "status": {"state": "failed"},
                    },
                }
            ],
        )

        self.assertFalse(summary["task_completed"])
        self.assertTrue(summary["final_response_is_error"])
        self.assertEqual(1, summary["failed_remote_tasks"])

    def test_process_metrics_use_actual_a2a_calls_not_rejected_model_calls(self):
        runner = ExperimentRunner.__new__(ExperimentRunner)
        runner.config = {
            "expected_agent_groups": [
                ["Weather Agent"],
                ["Guide Agent"],
            ],
            "exclusive_agent_groups": [],
        }
        events = [
            {
                "id": f"event-{index}",
                "content": {
                    "parts": [
                        {
                            "kind": "data",
                            "data": {
                                "name": "send_message",
                                "args": {
                                    "agent_name": agent,
                                    "message": agent,
                                },
                            },
                        }
                    ]
                },
            }
            for index, agent in enumerate(
                ["Weather Agent", "Hotel Agent", "Guide Agent"],
                start=1,
            )
        ]
        wire_trace = [
            {
                "direction": "outgoing",
                "phase": "business",
                "peer": agent,
                "payload": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": f"[label: {agent}]"}],
                },
            }
            for agent in ["Weather Agent", "Guide Agent"]
        ]
        summary = runner.analyze(
            run_id="boundary-run",
            mode_name="validation_on",
            prompt_id="travel",
            repetition=1,
            conversation="conversation-1",
            duration=1.0,
            timed_out=False,
            messages=[
                {
                    "role": "agent",
                    "parts": [{"kind": "text", "text": "完成"}],
                }
            ],
            events=events,
            tasks=[],
            log_text="",
            wire_trace=wire_trace,
        )

        self.assertTrue(summary["exact_protocol_sequence"])
        self.assertTrue(summary["strict_full_execution"])
        self.assertEqual(2, summary["business_send_message_calls"])
        self.assertEqual(3, summary["model_send_message_tool_calls"])
        self.assertEqual(1, summary["blocked_send_message_calls"])
        self.assertFalse(summary["repeated_agent_task"])
        self.assertEqual(0, summary["redundant_business_calls"])
        self.assertEqual(2, summary["required_stage_coverage_count"])
        self.assertEqual(2, summary["nonrepeat_business_calls"])
        self.assertEqual(1.0, summary["communication_efficiency"])

    def test_blocked_attempt_does_not_count_as_agent_coverage(self):
        runner = ExperimentRunner.__new__(ExperimentRunner)
        runner.config = {
            "expected_agent_groups": [["Weather Agent"]],
            "exclusive_agent_groups": [],
        }
        events = [
            {
                "id": "event-1",
                "content": {
                    "parts": [
                        {
                            "kind": "data",
                            "data": {
                                "name": "send_message",
                                "args": {"agent_name": "Weather Agent"},
                            },
                        }
                    ]
                },
            }
        ]
        # A non-business trace record proves boundary tracing was active, but
        # no business request actually crossed that boundary.
        wire_trace = [
            {
                "direction": "outgoing",
                "phase": "control",
                "peer": "Weather Agent",
                "payload": {},
            }
        ]

        summary = runner.analyze(
            run_id="blocked-run",
            mode_name="validation_on",
            prompt_id="travel",
            repetition=1,
            conversation="conversation-1",
            duration=1.0,
            timed_out=False,
            messages=[
                {
                    "role": "agent",
                    "parts": [{"kind": "text", "text": "已阻止非法调用"}],
                }
            ],
            events=events,
            tasks=[],
            log_text="",
            wire_trace=wire_trace,
        )

        self.assertEqual(0, summary["used_agent_count"])
        self.assertEqual(0, summary["required_stage_coverage_count"])
        self.assertEqual(0, summary["business_send_message_calls"])
        self.assertEqual(1, summary["blocked_send_message_calls"])

    def test_embedded_protocol_error_is_not_a_completed_output(self):
        runner = ExperimentRunner.__new__(ExperimentRunner)
        runner.config = {
            "expected_agent_groups": [["Weather Agent"]],
            "exclusive_agent_groups": [],
        }
        summary = runner.analyze(
            run_id="embedded-error",
            mode_name="validation_on",
            prompt_id="travel",
            repetition=1,
            conversation="conversation-1",
            duration=1.0,
            timed_out=False,
            messages=[
                {
                    "role": "agent",
                    "parts": [
                        {
                            "kind": "text",
                            "text": (
                                '### User: {"status": "error", '
                                '"code": "IncompleteProtocol"}'
                            ),
                        }
                    ],
                }
            ],
            events=[],
            tasks=[],
            log_text="",
            wire_trace=[],
        )
        self.assertTrue(summary["final_response_is_error"])
        self.assertFalse(summary["task_completed"])
        self.assertFalse(summary["final_output_usable"])
        self.assertEqual(0, summary["output_completeness_score_0_6"])

    def test_runs_and_exports_against_ui_contract(self):
        server = ThreadingHTTPServer(
            ("127.0.0.1", 0), _FakeConversationHandler
        )
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                config = {
                    "experiment_name": "contract-test",
                    "project_root": ".",
                    "output_root": "results",
                    "host_base_url": (
                        f"http://127.0.0.1:{server.server_port}"
                    ),
                    "repetitions": 1,
                    "poll_interval_seconds": 0.01,
                    "settle_seconds": 0,
                    "run_timeout_seconds": 5,
                    "prompts": [{"id": "p1", "text": "测试旅行计划"}],
                    "expected_agent_groups": [["Weather Agent"]],
                    "exclusive_agent_groups": [],
                    "services": [
                        {
                            "name": "Weather Agent",
                            "role": "remote",
                            "url": "http://127.0.0.1:9999",
                            "cwd": ".",
                            "command": ["python", "--version"],
                            "port": 9999,
                        }
                    ],
                }
                config_path = root / "experiment.json"
                config_path.write_text(
                    json.dumps(config, ensure_ascii=False),
                    encoding="utf-8",
                )
                runner = ExperimentRunner(
                    config_path,
                    mode_choice="on",
                    reuse_services=True,
                )
                result = runner.run()
                summary = (result / "summary.csv").read_text(
                    encoding="utf-8-sig"
                )
                self.assertIn("Weather Agent", summary)
                self.assertIn("10.0", summary)
                communication_files = list(
                    result.glob("validation_on/*/communications.csv")
                )
                self.assertEqual(len(communication_files), 1)
                self.assertIn(
                    "send_message",
                    communication_files[0].read_text(encoding="utf-8-sig"),
                )
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
