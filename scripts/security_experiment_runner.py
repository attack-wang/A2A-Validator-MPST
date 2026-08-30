"""Automate OP1 -> OP2 -> OP3 experiments and count validation errors.

This runner reuses the service orchestration and A2A capture implemented by
``experiment_runner.py``. It adds security-chain defaults plus structured
validation-error and model-recovery reports.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys

from collections import Counter
from pathlib import Path
from typing import Any

try:
    from .experiment_runner import (
        ERROR_FINAL_RE,
        TOOL_LEAK_RE,
        ExperimentRunner,
        csv_dump,
        json_dump,
        message_role,
        message_visible_text,
        safe_name,
    )
except ImportError:  # Direct execution: python scripts/security_experiment_runner.py
    from experiment_runner import (  # type: ignore[no-redef]
        ERROR_FINAL_RE,
        TOOL_LEAK_RE,
        ExperimentRunner,
        csv_dump,
        json_dump,
        message_role,
        message_visible_text,
        safe_name,
    )


SERVICE_HEADER_RE = re.compile(r"^=====\s+(.+?)\s+=====$")
HOST_FIELD_RE = re.compile(r"^\s{2}([^:]+):\s*(.*)$")
RECOVERY_MARKER = "[MPST RECOVERY]"
REMOTE_VIOLATION_MARKERS = (
    "MPST tool-call violation:",
    "MPST violation:",
)
EVENT_FIELDS = [
    "run_id",
    "mode",
    "prompt_id",
    "repetition",
    "sequence",
    "service",
    "event_type",
    "stage",
    "code",
    "error",
    "action",
    "role",
    "session_id",
    "attempt",
    "max_attempts",
    "current_position",
]
ERROR_METRIC_FIELDS = [
    "validation_error_count",
    "host_validation_error_count",
    "remote_validation_error_count",
    "recovery_retry_count",
    "recovery_success_count",
    "recovery_exhausted_count",
    "final_block_count",
    "run_had_validation_error",
]


def _empty_event(service: str, sequence: int) -> dict[str, Any]:
    return {
        "sequence": sequence,
        "service": service,
        "event_type": "",
        "stage": "",
        "code": "",
        "error": "",
        "action": "",
        "role": "",
        "session_id": "",
        "attempt": "",
        "max_attempts": "",
        "current_position": "",
    }


def _parse_mapping(text: str) -> dict[str, Any]:
    start = text.find("{")
    if start < 0:
        return {}
    payload = text[start:]
    try:
        value = json.loads(payload)
    except json.JSONDecodeError:
        try:
            value = ast.literal_eval(payload)
        except (SyntaxError, ValueError):
            return {}
    return value if isinstance(value, dict) else {}


def parse_validation_events(log_text: str) -> list[dict[str, Any]]:
    """Extract Host validation, Remote validation, and recovery events."""
    lines = log_text.splitlines()
    events: list[dict[str, Any]] = []
    service = "unknown"
    index = 0
    while index < len(lines):
        line = lines[index]
        header = SERVICE_HEADER_RE.match(line.strip())
        if header:
            service = header.group(1)
            index += 1
            continue

        if "[HOST VALIDATION ERROR]" in line:
            fields: dict[str, str] = {}
            cursor = index + 1
            while cursor < len(lines):
                match = HOST_FIELD_RE.match(lines[cursor])
                if not match:
                    break
                fields[match.group(1).strip().lower()] = match.group(2).strip()
                cursor += 1
            event = _empty_event(service, len(events) + 1)
            event.update(
                {
                    "event_type": "validation_error",
                    "stage": fields.get("stage", "host"),
                    "code": fields.get("code", "ProtocolViolation"),
                    "error": fields.get("error", ""),
                    "action": fields.get("action", ""),
                    "role": fields.get("peer", ""),
                    "session_id": fields.get("session", ""),
                    "current_position": fields.get("current position", ""),
                }
            )
            events.append(event)
            index = cursor
            continue

        if RECOVERY_MARKER in line:
            payload = _parse_mapping(line[line.index(RECOVERY_MARKER) :])
            if payload:
                event_name = str(payload.get("event") or "unknown")
                event = _empty_event(service, len(events) + 1)
                event.update(
                    {
                        "event_type": f"recovery_{event_name}",
                        "stage": "agent_output",
                        "code": payload.get("code", ""),
                        "error": payload.get("error", ""),
                        "role": payload.get("role", ""),
                        "session_id": payload.get("session_id", ""),
                        "attempt": payload.get("attempt", ""),
                        "max_attempts": payload.get("max_attempts", ""),
                        "current_position": payload.get(
                            "current_position", ""
                        ),
                    }
                )
                events.append(event)
            index += 1
            continue

        marker = next(
            (item for item in REMOTE_VIOLATION_MARKERS if item in line),
            None,
        )
        if marker:
            payload = _parse_mapping(line[line.index(marker) :])
            if payload:
                direction = str(payload.get("direction") or "output")
                event = _empty_event(service, len(events) + 1)
                event.update(
                    {
                        "event_type": "validation_error",
                        "stage": f"agent_{direction}",
                        "code": payload.get("code", "ProtocolViolation"),
                        "error": payload.get("error", ""),
                        "role": payload.get("peer", ""),
                        "current_position": payload.get(
                            "position", ""
                        ),
                    }
                )
                events.append(event)
        index += 1
    return events


def _counter_text(values: list[str]) -> str:
    counts = Counter(value for value in values if value)
    return "|".join(f"{key}:{counts[key]}" for key in sorted(counts))


def summarize_validation_events(
    validation_events: list[dict[str, Any]],
) -> dict[str, Any]:
    errors = [
        event
        for event in validation_events
        if event.get("event_type") == "validation_error"
    ]
    retries = [
        event
        for event in validation_events
        if event.get("event_type") == "recovery_retry"
    ]
    recovered = [
        event
        for event in validation_events
        if event.get("event_type") == "recovery_recovered"
    ]
    exhausted = [
        event
        for event in validation_events
        if event.get("event_type") == "recovery_exhausted"
    ]
    host_errors = [
        event
        for event in errors
        if str(event.get("stage", "")).startswith("host_")
        or event.get("service") == "Host UI"
    ]
    final_host_actions = {
        "rejected_after_retry_limit",
        "visible_error_returned",
        "workflow_not_finalized",
    }
    final_blocks = len(exhausted) + sum(
        event.get("action") in final_host_actions for event in errors
    )
    return {
        "validation_error_count": len(errors),
        "host_validation_error_count": len(host_errors),
        "remote_validation_error_count": len(errors) - len(host_errors),
        "validation_error_codes": _counter_text(
            [str(event.get("code", "")) for event in errors]
        ),
        "validation_error_stages": _counter_text(
            [str(event.get("stage", "")) for event in errors]
        ),
        "recovery_retry_count": len(retries),
        "recovery_success_count": len(recovered),
        "recovery_exhausted_count": len(exhausted),
        "final_block_count": final_blocks,
        "run_had_validation_error": bool(errors),
    }


class SecurityExperimentRunner(ExperimentRunner):
    """OP1/OP2/OP3 runner with validation-error accounting."""

    def analyze(
        self,
        run_id: str,
        mode_name: str,
        prompt_id: str,
        repetition: int,
        conversation: str,
        duration: float,
        timed_out: bool,
        messages: list[dict[str, Any]],
        events: list[dict[str, Any]],
        tasks: list[dict[str, Any]],
        log_text: str,
        wire_trace: list[dict[str, Any]],
    ) -> dict[str, Any]:
        summary = super().analyze(
            run_id,
            mode_name,
            prompt_id,
            repetition,
            conversation,
            duration,
            timed_out,
            messages,
            events,
            tasks,
            log_text,
            wire_trace,
        )
        validation_events = parse_validation_events(log_text)
        summary.update(summarize_validation_events(validation_events))

        agent_messages = [
            item for item in messages if message_role(item).lower() == "agent"
        ]
        final_text = (
            message_visible_text(agent_messages[-1]) if agent_messages else ""
        )
        minimum_chars = int(self.config.get("minimum_final_chars", 20))
        summary["final_output_usable"] = bool(
            summary["task_completed"]
            and not TOOL_LEAK_RE.search(final_text)
            and not ERROR_FINAL_RE.search(final_text)
            and len(final_text.strip()) >= minimum_chars
        )
        summary["strict_full_execution"] = bool(
            summary["task_completed"]
            and summary["exact_protocol_sequence"]
            and summary["failed_remote_tasks"] == 0
            and not summary["tool_call_leak_in_final"]
        )
        expected = next(
            (
                str(prompt.get("expected_final_output") or "")
                for prompt in self.config.get("prompts", [])
                if str(prompt.get("id")) == prompt_id
            ),
            "",
        )
        summary["expected_final_output"] = expected
        summary["final_output_matches_expected"] = bool(
            expected and expected in final_text
        )
        return summary

    def _combined_run_logs(self, run_dir: Path) -> str:
        service_names = {
            safe_name(str(service["name"])): str(service["name"])
            for service in self.config["services"]
        }
        sections = []
        for path in sorted((run_dir / "process_logs").glob("*.log")):
            service_name = service_names.get(path.stem, path.stem)
            sections.append(
                f"===== {service_name} =====\n"
                + path.read_text(encoding="utf-8", errors="replace")
            )
        return "\n".join(sections)

    def write_tables(self) -> None:
        super().write_tables()
        all_events: list[dict[str, Any]] = []
        for mode_name, _ in self.modes():
            mode_dir = self.session_dir / mode_name
            for run_path in sorted(mode_dir.glob("*/run.json")):
                run_dir = run_path.parent
                run = json.loads(run_path.read_text(encoding="utf-8"))
                parsed = parse_validation_events(
                    self._combined_run_logs(run_dir)
                )
                enriched = []
                for event in parsed:
                    row = {
                        "run_id": run.get("run_id", run_dir.name),
                        "mode": run.get("mode", mode_name),
                        "prompt_id": run.get("prompt_id", ""),
                        "repetition": run.get("repetition", ""),
                        **event,
                    }
                    enriched.append(row)
                    all_events.append(row)
                json_dump(run_dir / "validation_events.json", enriched)
                csv_dump(
                    run_dir / "validation_events.csv",
                    enriched,
                    EVENT_FIELDS,
                )

        csv_dump(
            self.session_dir / "validation_events.csv",
            all_events,
            EVENT_FIELDS,
        )
        error_counts = Counter(
            (
                str(event.get("mode", "")),
                str(event.get("service", "")),
                str(event.get("stage", "")),
                str(event.get("code", "")),
            )
            for event in all_events
            if event.get("event_type") == "validation_error"
        )
        error_rows = [
            {
                "mode": key[0],
                "service": key[1],
                "stage": key[2],
                "code": key[3],
                "count": count,
            }
            for key, count in sorted(error_counts.items())
        ]
        csv_dump(
            self.session_dir / "error_counts.csv",
            error_rows,
            ["mode", "service", "stage", "code", "count"],
        )

        aggregate_rows = []
        for mode_name, _ in self.modes():
            selected = [
                row for row in self.summary_rows if row["mode"] == mode_name
            ]
            if not selected:
                continue
            aggregate: dict[str, Any] = {
                "mode": mode_name,
                "runs": len(selected),
            }
            for field in ERROR_METRIC_FIELDS:
                total = sum(float(row.get(field, 0)) for row in selected)
                aggregate[f"total_{field}"] = round(total, 4)
                aggregate[f"mean_{field}"] = round(total / len(selected), 4)
            aggregate_rows.append(aggregate)
        if aggregate_rows:
            csv_dump(
                self.session_dir / "error_aggregate.csv",
                aggregate_rows,
                list(aggregate_rows[0].keys()),
            )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automate OP1/OP2/OP3 experiments and count MPST errors."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/security_chain_experiment.json"),
    )
    parser.add_argument(
        "--mode",
        choices=("both", "on", "off"),
        default="both",
    )
    parser.add_argument("--repetitions", type=int)
    parser.add_argument("--reuse-services", action="store_true")
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--resume-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.repetitions is not None and args.repetitions < 1:
        raise ValueError("--repetitions must be at least 1")
    runner = SecurityExperimentRunner(
        args.config,
        mode_choice=args.mode,
        repetitions=args.repetitions,
        reuse_services=args.reuse_services,
        output_root=args.output_root,
        resume_dir=args.resume_dir,
    )
    result = runner.dry_run() if args.dry_run else runner.run()
    print(f"Security experiment results: {result}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Experiment interrupted by user.", file=sys.stderr)
        raise SystemExit(130)
