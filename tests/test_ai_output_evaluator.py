from __future__ import annotations

import json
import tempfile
import unittest

from pathlib import Path

from scripts.evaluate_outputs import (
    aggregate_rows,
    discover_runs,
    extract_json_object,
    load_final_output,
    normalize_judgment,
    score_rows,
)


def complete_judgment(value: bool = True):
    return {
        key: {"satisfied": value, "evidence": key, "reason": ""}
        for key in (
            "transport",
            "hotel",
            "tickets",
            "weather",
            "daily_routes",
            "budget",
        )
    }


class AIOutputEvaluatorTests(unittest.TestCase):
    def test_extracts_and_normalizes_fenced_json(self):
        raw = "```json\n" + json.dumps(complete_judgment()) + "\n```"
        normalized = normalize_judgment(extract_json_object(raw))
        self.assertTrue(normalized["budget"]["satisfied"])

    def test_rejects_non_boolean_scores(self):
        value = complete_judgment()
        value["transport"]["satisfied"] = 1
        with self.assertRaises(ValueError):
            normalize_judgment(value)

    def test_reads_final_agent_message_and_scores(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "validation_on" / "run-1"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps(
                    {
                        "run_id": "run-1",
                        "mode": "validation_on",
                        "prompt_id": "travel",
                        "repetition": 1,
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "messages.json").write_text(
                json.dumps(
                    [
                        {"role": "user", "parts": [{"kind": "text", "text": "q"}]},
                        {"role": "agent", "parts": [{"kind": "text", "text": "final"}]},
                    ]
                ),
                encoding="utf-8",
            )
            self.assertEqual("final", load_final_output(run_dir))
            self.assertEqual(1, len(discover_runs(root)))

        judgments = [
            {
                "run_id": "run-1",
                "mode": "validation_on",
                "prompt_id": "travel",
                "repetition": 1,
                "judge_model": "judge",
                "status": "ok",
                "judgment": complete_judgment(),
            }
        ]
        rows = score_rows(judgments)
        self.assertEqual(6, rows[0]["ai_output_quality_score_0_6"])
        aggregate = aggregate_rows(rows)
        self.assertEqual(6.0, aggregate[0]["mean_ai_output_quality_score_0_6"])


if __name__ == "__main__":
    unittest.main()
