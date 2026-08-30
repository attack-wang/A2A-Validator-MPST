"""Evaluate travel-plan final outputs with a pinned AI judge.

The evaluator reads completed experiment run directories, sends only the final
Host response to the configured Ollama model, validates the six-item JSON
judgment, and preserves both raw responses and normalized scores.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request

from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from .experiment_runner import (
        csv_dump,
        json_dump,
        message_role,
        message_visible_text,
        reproducibility_metadata,
    )
except ImportError:  # Direct execution from the repository root.
    from experiment_runner import (  # type: ignore[no-redef]
        csv_dump,
        json_dump,
        message_role,
        message_visible_text,
        reproducibility_metadata,
    )


CRITERIA = (
    "transport",
    "hotel",
    "tickets",
    "weather",
    "daily_routes",
    "budget",
)


def load_final_output(run_dir: Path) -> str:
    messages_path = run_dir / "messages.json"
    if not messages_path.exists():
        return ""
    messages = json.loads(messages_path.read_text(encoding="utf-8"))
    agent_messages = [
        item
        for item in messages
        if message_role(item).lower() == "agent"
    ]
    return message_visible_text(agent_messages[-1]) if agent_messages else ""


def extract_json_object(text: str) -> dict[str, Any]:
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = re.sub(r"^```(?:json)?\s*", "", candidate)
        candidate = re.sub(r"\s*```$", "", candidate)
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("Judge response does not contain a JSON object")
        parsed = json.loads(candidate[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("Judge response root must be a JSON object")
    return parsed


def normalize_judgment(value: dict[str, Any]) -> dict[str, dict[str, Any]]:
    normalized: dict[str, dict[str, Any]] = {}
    for criterion in CRITERIA:
        item = value.get(criterion)
        if not isinstance(item, dict):
            raise ValueError(f"Missing object for criterion {criterion!r}")
        satisfied = item.get("satisfied")
        if not isinstance(satisfied, bool):
            raise ValueError(
                f"Criterion {criterion!r} must contain boolean satisfied"
            )
        normalized[criterion] = {
            "satisfied": satisfied,
            "evidence": str(item.get("evidence", "")).strip(),
            "reason": str(item.get("reason", "")).strip(),
        }
    return normalized


def call_ollama(
    prompt: str,
    config: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], str]:
    payload = {
        "model": config["model"],
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {
            "temperature": config.get("temperature", 0),
            "seed": config.get("seed", 20260830),
        },
    }
    request = urllib.request.Request(
        str(config["api_url"]),
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    attempts = int(config.get("max_attempts", 3))
    timeout = float(config.get("timeout_seconds", 180))
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
            raw = str((body.get("message") or {}).get("content", ""))
            return normalize_judgment(extract_json_object(raw)), raw
        except (
            OSError,
            ValueError,
            KeyError,
            TypeError,
            json.JSONDecodeError,
            urllib.error.URLError,
        ) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(min(2**attempt, 4))
    raise RuntimeError(f"AI judge failed after {attempts} attempts: {last_error}")


def discover_runs(results_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    discovered = []
    for run_path in sorted(results_dir.glob("validation_*/*/run.json")):
        try:
            run = json.loads(run_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        discovered.append((run_path.parent, run))
    return discovered


def score_rows(judgments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for item in judgments:
        judgment = item.get("judgment") or {}
        row: dict[str, Any] = {
            "run_id": item["run_id"],
            "mode": item["mode"],
            "prompt_id": item["prompt_id"],
            "repetition": item["repetition"],
            "judge_status": item["status"],
            "judge_model": item["judge_model"],
        }
        total = 0
        for criterion in CRITERIA:
            criterion_value = judgment.get(criterion, {})
            score = int(bool(criterion_value.get("satisfied", False)))
            row[f"{criterion}_0_1"] = score
            row[f"{criterion}_evidence"] = criterion_value.get("evidence", "")
            row[f"{criterion}_reason"] = criterion_value.get("reason", "")
            total += score
        row["ai_output_quality_score_0_6"] = total
        rows.append(row)
    return rows


def aggregate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["mode"])].append(row)
    output = []
    for mode, selected in sorted(grouped.items()):
        successful = [row for row in selected if row["judge_status"] == "ok"]
        divisor = len(successful) or 1
        aggregate: dict[str, Any] = {
            "mode": mode,
            "runs": len(selected),
            "successfully_judged_runs": len(successful),
        }
        for criterion in CRITERIA:
            aggregate[f"mean_{criterion}_0_1"] = round(
                sum(float(row[f"{criterion}_0_1"]) for row in successful)
                / divisor,
                4,
            )
        aggregate["mean_ai_output_quality_score_0_6"] = round(
            sum(
                float(row["ai_output_quality_score_0_6"])
                for row in successful
            )
            / divisor,
            4,
        )
        output.append(aggregate)
    return output


def evaluate(
    results_dir: Path,
    config_path: Path,
    *,
    dry_run: bool = False,
    limit: int | None = None,
) -> Path:
    results_dir = results_dir.resolve()
    config_path = config_path.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    prompt_path = (config_path.parent / config["prompt_file"]).resolve()
    template = prompt_path.read_text(encoding="utf-8")
    runs = discover_runs(results_dir)
    if limit is not None:
        runs = runs[:limit]
    if not runs:
        raise ValueError(f"No completed run.json files found in {results_dir}")

    if dry_run:
        run_dir, run = runs[0]
        prompt = template.replace(
            "{final_output}", load_final_output(run_dir)
        )
        output = results_dir / "ai_judge_prompt.preview.txt"
        output.write_text(prompt, encoding="utf-8")
        return output

    judgments = []
    for index, (run_dir, run) in enumerate(runs, start=1):
        final_output = load_final_output(run_dir)
        base = {
            "run_id": str(run.get("run_id", run_dir.name)),
            "mode": str(run.get("mode", "")),
            "prompt_id": str(run.get("prompt_id", "")),
            "repetition": run.get("repetition", ""),
            "judge_model": str(config["model"]),
        }
        if not final_output.strip():
            judgments.append(
                {
                    **base,
                    "status": "no_final_output",
                    "judgment": {},
                    "raw_response": "",
                }
            )
            continue
        prompt = template.replace("{final_output}", final_output)
        print(f"[{index}/{len(runs)}] judging {base['run_id']}...")
        try:
            judgment, raw = call_ollama(prompt, config)
            judgments.append(
                {
                    **base,
                    "status": "ok",
                    "judgment": judgment,
                    "raw_response": raw,
                }
            )
        except RuntimeError as exc:
            judgments.append(
                {
                    **base,
                    "status": "error",
                    "judgment": {},
                    "raw_response": str(exc),
                }
            )

    rows = score_rows(judgments)
    json_dump(results_dir / "ai_judgments.json", judgments)
    csv_dump(results_dir / "ai_output_scores.csv", rows, list(rows[0].keys()))
    aggregates = aggregate_rows(rows)
    if aggregates:
        csv_dump(
            results_dir / "ai_score_aggregate.csv",
            aggregates,
            list(aggregates[0].keys()),
        )
    metadata = {
        "judge_config": config,
        "prompt_file": str(prompt_path),
        "evaluated_runs": len(rows),
        "reproducibility": reproducibility_metadata(
            Path(__file__).resolve().parents[1]
        ),
    }
    json_dump(results_dir / "ai_judge_manifest.json", metadata)
    return results_dir / "ai_output_scores.csv"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate travel final outputs with a fixed AI judge."
    )
    parser.add_argument("results_dir", type=Path)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/ai_judge_config.json"),
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.limit is not None and args.limit < 1:
        raise ValueError("--limit must be at least 1")
    output = evaluate(
        args.results_dir,
        args.config,
        dry_run=args.dry_run,
        limit=args.limit,
    )
    print(f"AI evaluation output: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
