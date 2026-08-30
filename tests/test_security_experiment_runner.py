from __future__ import annotations

import json
import tempfile
import unittest

from pathlib import Path

from scripts.security_experiment_runner import (
    SecurityExperimentRunner,
    parse_validation_events,
    summarize_validation_events,
)


class SecurityExperimentRunnerTests(unittest.TestCase):
    def test_parses_host_remote_and_recovery_events(self):
        log_text = """===== Host UI =====
2026-08-08 ERROR host.validation [HOST VALIDATION ERROR]
  Stage: host_send
  Code: WrongOrder
  Error: Expected OP1 before OP2
  Session: session-host
  Peer: OP2
  Current position: state-1
  Expected transitions: OP1
  Content: OP2 request
  Action: rejected_before_remote_send
===== IP Intelligence Agent =====
WARNING:mpst_ext.mpst_validator:MPST violation: {'code': 'WrongType', 'direction': 'send', 'peer': 'Host', 'error': 'expected number', 'position': 'state-2'}
WARNING:mpst_ext.mpst_validation_ext:[MPST RECOVERY] {"event":"retry","role":"OP1","session_id":"session-agent","code":"WrongType","error":"expected number","attempt":1,"max_attempts":2,"current_position":"state-2"}
INFO:mpst_ext.mpst_validation_ext:[MPST RECOVERY] {"event":"recovered","role":"OP1","session_id":"session-agent","code":"WrongType","error":"expected number","attempt":1,"max_attempts":2,"current_position":"state-2"}
"""

        events = parse_validation_events(log_text)
        summary = summarize_validation_events(events)

        self.assertEqual(4, len(events))
        self.assertEqual("Host UI", events[0]["service"])
        self.assertEqual("rejected_before_remote_send", events[0]["action"])
        self.assertEqual("agent_send", events[1]["stage"])
        self.assertEqual(2, summary["validation_error_count"])
        self.assertEqual(1, summary["host_validation_error_count"])
        self.assertEqual(1, summary["remote_validation_error_count"])
        self.assertEqual("WrongOrder:1|WrongType:1", summary["validation_error_codes"])
        self.assertEqual(1, summary["recovery_retry_count"])
        self.assertEqual(1, summary["recovery_success_count"])
        self.assertEqual(0, summary["recovery_exhausted_count"])
        self.assertEqual(0, summary["final_block_count"])
        self.assertTrue(summary["run_had_validation_error"])

    def test_counts_exhausted_recovery_as_final_block(self):
        log_text = """===== Defense Strategy Agent =====
ERROR:mpst_ext.mpst_validation_ext:[MPST RECOVERY] {"event":"exhausted","role":"OP3","session_id":"session-3","code":"WrongLabel","error":"wrong label","attempt":2,"max_attempts":2,"current_position":"state-3"}
"""

        summary = summarize_validation_events(
            parse_validation_events(log_text)
        )

        self.assertEqual(0, summary["validation_error_count"])
        self.assertEqual(1, summary["recovery_exhausted_count"])
        self.assertEqual(1, summary["final_block_count"])

    def test_ignores_malformed_marker_payloads(self):
        events = parse_validation_events(
            "===== OP1 =====\n[MPST RECOVERY] not-json\n"
            "MPST violation: not-a-mapping"
        )

        self.assertEqual([], events)

    def test_analyze_adds_error_and_expected_output_metrics(self):
        runner = SecurityExperimentRunner.__new__(SecurityExperimentRunner)
        runner.config = {
            "minimum_final_chars": 20,
            "expected_agent_groups": [
                ["IP Intelligence Agent"],
                ["Weapon Library Asset Agent"],
                ["Defense Strategy Agent"],
            ],
            "exclusive_agent_groups": [],
            "prompts": [
                {
                    "id": "security-chain-x",
                    "expected_final_output": "Block_Rule_Protocol_v3.sh",
                }
            ],
            "services": [{"name": "Host UI"}],
        }
        peers = [
            "IP Intelligence Agent",
            "Weapon Library Asset Agent",
            "Defense Strategy Agent",
        ]
        wire_trace = [
            {
                "direction": "outgoing",
                "phase": "business",
                "peer": peer,
                "payload": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": peer}],
                },
            }
            for peer in peers
        ]

        summary = runner.analyze(
            run_id="security-run",
            mode_name="validation_on",
            prompt_id="security-chain-x",
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
                                "威胁分析完成，防御脚本为 "
                                "Block_Rule_Protocol_v3.sh"
                            ),
                        }
                    ],
                }
            ],
            events=[],
            tasks=[],
            log_text=(
                "===== Host UI =====\n"
                "[HOST VALIDATION ERROR]\n"
                "  Stage: host_send\n"
                "  Code: WrongOrder\n"
                "  Error: wrong order\n"
                "  Action: rejected_before_remote_send\n"
            ),
            wire_trace=wire_trace,
        )

        self.assertEqual(1, summary["validation_error_count"])
        self.assertTrue(summary["final_output_usable"])
        self.assertTrue(summary["strict_full_execution"])
        self.assertTrue(summary["final_output_matches_expected"])

        with tempfile.TemporaryDirectory() as temp_dir:
            runner.session_dir = Path(temp_dir)
            runner.mode_choice = "on"
            runner.repetitions = 1
            runner.prompts = runner.config["prompts"]
            runner.summary_rows = [summary]
            run_dir = runner.session_dir / "validation_on" / "security-run"
            log_dir = run_dir / "process_logs"
            log_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps(summary, ensure_ascii=False),
                encoding="utf-8",
            )
            (log_dir / "Host-UI.log").write_text(
                "[HOST VALIDATION ERROR]\n"
                "  Stage: host_send\n"
                "  Code: WrongOrder\n"
                "  Error: wrong order\n"
                "  Action: rejected_before_remote_send\n",
                encoding="utf-8",
            )

            runner.write_tables()

            error_counts = (runner.session_dir / "error_counts.csv").read_text(
                encoding="utf-8-sig"
            )
            self.assertIn("Host UI,host_send,WrongOrder,1", error_counts)
            self.assertTrue(
                (runner.session_dir / "error_aggregate.csv").exists()
            )
            self.assertTrue((run_dir / "validation_events.json").exists())


if __name__ == "__main__":
    unittest.main()
