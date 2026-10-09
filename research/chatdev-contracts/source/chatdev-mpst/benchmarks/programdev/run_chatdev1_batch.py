"""Run the complete ProgramDev dataset as paired ChatDev 1.0 experiments.

Run one condition at a time so the two conditions do not contend for Ollama.
Progress and per-task evaluations are saved after every run. Existing runs
are never overwritten. This is intentionally a separate, unattended driver.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

import evaluate


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "benchmarks" / "programdev"
RUNNER = HERE / "run_chatdev1_task.py"
DATASET = HERE / "programdev_dataset.json"
RUNS = HERE / "runs"
CONFIG = ROOT / "integrations" / "ChatDev1.0" / "CompanyConfig" / "MPSTPilot" / "ChatChainConfig.json"
PROVENANCE_FILES = (
    DATASET,
    RUNNER,
    CONFIG,
    ROOT / "integrations" / "ChatDev1.0" / "camel" / "model_backend.py",
    ROOT / "integrations" / "ChatDev1.0" / "camel" / "agents" / "chat_agent.py",
    ROOT / "integrations" / "ChatDev1.0" / "chatdev" / "phase.py",
    ROOT / "integrations" / "ChatDev1.0" / "chatdev" / "mpst_global.py",
    ROOT / "integrations" / "ChatDev1.0" / "chatdev" / "mpst_pilot.py",
    ROOT / "integrations" / "ChatDev1.0" / "protocol" / "mpst_global_pilot.gt",
    HERE / "evaluate.py",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-name", required=True)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--model", default="glm-5.3-flash:cloud")
    parser.add_argument("--judge-model", default="gpt-oss:120b-cloud")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.batch_name):
        parser.error("batch-name may contain only letters, digits, dots, underscores, and hyphens")
    if args.timeout < 60:
        parser.error("timeout must be at least 60 seconds")
    return args


def file_hashes() -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in PROVENANCE_FILES
    }


def save_json(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(temporary, path)


def keep_windows_awake() -> None:
    if sys.platform == "win32":
        # This lasts only while this process is alive; it does not change the
        # machine's saved power plan or prevent the display from turning off.
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)


def permit_windows_sleep() -> None:
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)


def main() -> int:
    args = parse_args()
    tasks = json.loads(DATASET.read_text(encoding="utf-8"))
    if len(tasks) != 30:
        raise SystemExit(f"Expected 30 ProgramDev tasks, found {len(tasks)}")
    tags = {condition: f"{args.batch_name}_{condition}" for condition in ("off", "global")}
    batch_dir = RUNS / f"{args.batch_name}_batch"
    schedule = [
        (index, condition)
        for index in range(len(tasks))
        for condition in (("off", "global") if index % 2 == 0 else ("global", "off"))
    ]
    if args.dry_run:
        print(json.dumps({
            "tasks": len(tasks), "runs": len(schedule), "tags": tags,
            "first_four": schedule[:4], "last_four": schedule[-4:],
            "timeout_seconds": args.timeout, "model": args.model,
            "judge_model": args.judge_model,
        }, indent=2))
        return 0
    hashes = file_hashes()
    progress_path = batch_dir / "progress.json"
    manifest_path = batch_dir / "manifest.json"
    if args.resume:
        if not manifest_path.is_file() or not progress_path.is_file():
            raise SystemExit("Cannot resume: manifest.json or progress.json is missing")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        expected = {
            "dataset_size": len(tasks), "tags": tags, "model": args.model,
            "judge_model": args.judge_model, "timeout_seconds": args.timeout,
        }
        mismatches = [key for key, value in expected.items() if manifest.get(key) != value]
        if mismatches:
            raise SystemExit("Cannot resume with changed settings: " + ", ".join(mismatches))
        original_hashes = manifest.get("file_sha256", {})
        changed = [key for key, value in hashes.items() if original_hashes.get(key) != value]
        if changed:
            raise SystemExit("Cannot resume because experiment files changed: " + ", ".join(changed))
        started = manifest["started_at"]
        progress["state"] = "running"
        progress["finished_at"] = None
        progress["process_id"] = os.getpid()
        progress["current"] = None
        progress.pop("fatal_error", None)
        progress["resume_count"] = int(progress.get("resume_count", 0)) + 1
        progress["last_resumed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        save_json(progress_path, progress)
        print(f"Resuming after {progress['completed_runs']} completed runs; progress: {progress_path}", flush=True)
    else:
        occupied = [str(path) for path in [batch_dir, *(RUNS / tag for tag in tags.values())] if path.exists()]
        if occupied:
            raise SystemExit("Refusing to overwrite existing batch paths: " + ", ".join(occupied))
        batch_dir.mkdir(parents=True)
        started = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        manifest = {
            "batch_name": args.batch_name,
            "started_at": started,
            "dataset_size": len(tasks),
            "planned_runs": len(schedule),
            "tags": tags,
            "model": args.model,
            "judge_model": args.judge_model,
            "timeout_seconds": args.timeout,
            "schedule": [{"task_index": i, "condition": c} for i, c in schedule],
            "file_sha256": hashes,
            "python": sys.executable,
        }
        save_json(manifest_path, manifest)
        progress = {
            "state": "running", "started_at": started, "finished_at": None,
            "process_id": os.getpid(),
            "completed_runs": 0, "planned_runs": len(schedule),
            "current": None, "runs": [],
        }
        save_json(progress_path, progress)
        print(f"Starting {len(schedule)} runs; progress: {progress_path}", flush=True)
    completed_keys = {(item["task_index"], item["condition"]) for item in progress["runs"]}
    keep_windows_awake()
    try:
        for index, condition in schedule:
            if (index, condition) in completed_keys:
                continue
            if file_hashes() != hashes:
                raise RuntimeError("Experiment source/config changed during batch; stopped to preserve comparability")
            task = tasks[index]
            tag = tags[condition]
            run_dir = RUNS / tag / "chatdev" / f"{index:02d}_{task['project_name']}"
            if run_dir.exists() and not (run_dir / "run_result.json").is_file():
                interrupted_dir = run_dir.with_name(
                    run_dir.name + ".interrupted_" + time.strftime("%Y%m%d%H%M%S")
                )
                run_dir.rename(interrupted_dir)
                print(f"  preserved interrupted output at {interrupted_dir}", flush=True)
            elif run_dir.exists():
                raise RuntimeError(f"Unrecorded completed run exists: {run_dir}")
            progress["current"] = {
                "task_index": index, "project_name": task["project_name"],
                "condition": condition, "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            }
            save_json(progress_path, progress)
            print(f"[{progress['completed_runs'] + 1}/{len(schedule)}] {index:02d} {task['project_name']} {condition}", flush=True)
            command = [
                sys.executable, str(RUNNER), "--index", str(index),
                "--run-tag", tag, "--mpst-scope", condition,
                "--timeout", str(args.timeout), "--model", args.model,
            ]
            began = time.monotonic()
            try:
                result = subprocess.run(
                    command, cwd=ROOT, capture_output=True, text=True,
                    encoding="utf-8", errors="replace", timeout=args.timeout + 120,
                    check=False,
                )
                runner_status = "ok" if result.returncode == 0 else "failed"
                runner_message = (result.stdout + result.stderr)[-2000:]
            except subprocess.TimeoutExpired as exc:
                runner_status = "driver_timeout"
                runner_message = str(exc)
            except Exception as exc:
                runner_status = "driver_error"
                runner_message = f"{type(exc).__name__}: {exc}"
            evaluation = None
            evaluation_error = None
            result_path = run_dir / "run_result.json"
            if result_path.is_file():
                judge_args = argparse.Namespace(
                    no_judge=False, rerun_judge=False,
                    max_source_chars=60000, judge_model=args.judge_model,
                    base_url="http://127.0.0.1:11434/v1",
                )
                try:
                    evaluation = evaluate.evaluate_run(run_dir, task, judge_args)
                except Exception as exc:
                    evaluation_error = f"{type(exc).__name__}: {exc}"
            else:
                evaluation_error = "run_result.json is missing"
            record = {
                "task_index": index, "project_name": task["project_name"],
                "condition": condition, "run_tag": tag,
                "runner_status": runner_status,
                "runner_message": runner_message,
                "elapsed_seconds": round(time.monotonic() - began, 3),
                "workflow_status": evaluation.get("workflow_status") if evaluation else None,
                "artifact_pass": evaluation.get("artifact_pass") if evaluation else None,
                "evaluation_error": evaluation_error,
                "result_path": str(result_path) if result_path.is_file() else None,
            }
            progress["runs"].append(record)
            progress["completed_runs"] = len(progress["runs"])
            progress["current"] = None
            save_json(progress_path, progress)
            print(
                f"  runner={runner_status} workflow={record['workflow_status']} "
                f"artifact_pass={record['artifact_pass']} elapsed={record['elapsed_seconds']}s",
                flush=True,
            )
        progress["state"] = "complete"
    except Exception:
        progress["state"] = "stopped"
        progress["fatal_error"] = traceback.format_exc()
        print(progress["fatal_error"], file=sys.stderr, flush=True)
    finally:
        permit_windows_sleep()
        progress["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        progress["current"] = None
        save_json(progress_path, progress)
        by_condition = {}
        for condition in ("off", "global"):
            items = [item for item in progress["runs"] if item["condition"] == condition]
            by_condition[condition] = {
                "planned": len(tasks), "evaluated": len(items),
                "artifact_passed": sum(item["artifact_pass"] is True for item in items),
                "workflow_completed": sum(item["workflow_status"] == "completed" for item in items),
                "evaluation_errors": sum(item["evaluation_error"] is not None for item in items),
            }
        summary = {
            "state": progress["state"], "batch_name": args.batch_name,
            "started_at": started, "finished_at": progress["finished_at"],
            "comparable_to_paper_human_accuracy": False,
            "evaluation_method": "syntax/import/self-test gate plus Ollama Cloud requirement judge",
            "conditions": by_condition,
        }
        save_json(batch_dir / "summary.json", summary)
        print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)
    return 0 if progress["state"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
