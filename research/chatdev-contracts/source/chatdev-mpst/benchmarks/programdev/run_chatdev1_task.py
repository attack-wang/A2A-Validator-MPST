"""Run one ProgramDev task through the isolated ChatDev 1.0 worktree.

Use a fresh run tag for each condition. This runner never deletes existing
results or modifies the ChatDev 2.0 checkout.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "benchmarks" / "programdev"
LEGACY = ROOT / "integrations" / "ChatDev1.0"
PYTHON = LEGACY / ".venv" / "Scripts" / "python.exe"
WAREHOUSE = LEGACY / "WareHouse"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--run-tag", required=True)
    parser.add_argument("--mpst-scope", choices=("off", "global"), required=True)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--model", default="glm-5.3-flash:cloud")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.run_tag):
        parser.error("run-tag may contain only letters, digits, dots, underscores, and hyphens")
    tasks = json.loads((HERE / "programdev_dataset.json").read_text(encoding="utf-8"))
    if not 0 <= args.index < len(tasks):
        parser.error("index is outside the dataset")
    if not PYTHON.is_file():
        parser.error("ChatDev 1.0 virtual environment is missing")

    task = tasks[args.index]
    project = task["project_name"]
    run_dir = HERE / "runs" / args.run_tag / "chatdev" / f"{args.index:02d}_{project}"
    if run_dir.exists():
        parser.error(f"result directory already exists: {run_dir}")
    run_dir.mkdir(parents=True)

    name = f"PD{args.index:02d}{project}"
    org = args.run_tag
    prefix = f"{name}_{org}_"
    before = {item.name for item in WAREHOUSE.glob(prefix + "*")}

    env = os.environ.copy()
    env.update({
        "PYTHONIOENCODING": "utf-8",
        "OPENAI_API_KEY": env.get("OPENAI_API_KEY") or "ollama",
        "BASE_URL": "http://127.0.0.1:11434/v1",
        "CHATDEV_MODEL_NAME": args.model,
        "CHATDEV_CONTEXT_LIMIT": "32768",
        "CHATDEV_MAX_TOKENS": "8192",
        "CHATDEV_REASONING_EFFORT": "none",
    })
    if args.mpst_scope == "global":
        env.update({
            "CHATDEV_MPST_ENABLED": "1",
            "CHATDEV_MPST_SCOPE": "global",
            "CHATDEV_MPST_MAX_RETRIES": "2",
        })
    else:
        env.pop("CHATDEV_MPST_ENABLED", None)
        env.pop("CHATDEV_MPST_SCOPE", None)
        env.pop("CHATDEV_MPST_MAX_RETRIES", None)

    command = [
        str(PYTHON), "run.py", "--config", "MPSTPilot", "--org", org,
        "--task", task["description"], "--name", name, "--model", "GPT_4O",
    ]
    started = time.monotonic()
    status = "failed"
    error = None
    with (run_dir / "console.log").open("w", encoding="utf-8", errors="replace") as output:
        try:
            completed = subprocess.run(
                command, cwd=LEGACY, env=env, stdout=output,
                stderr=subprocess.STDOUT, timeout=args.timeout, check=False,
            )
            status = "completed" if completed.returncode == 0 else "failed"
            if completed.returncode:
                error = f"exit code {completed.returncode}"
        except subprocess.TimeoutExpired:
            status = "timeout"
            error = f"exceeded {args.timeout} seconds"
    elapsed = round(time.monotonic() - started, 3)
    created = sorted(
        (item for item in WAREHOUSE.glob(prefix + "*")
         if item.is_dir() and item.name not in before),
        key=lambda item: item.stat().st_mtime,
    )
    project_path = created[-1] if created else None
    result = {
        "task_index": args.index,
        "project_name": project,
        "description": task["description"],
        "framework": "ChatDev",
        "framework_version": "1.0 (chatdev1.0 branch, commit 31fd994416a251ecdeb1f0a73c329271743bfb56)",
        "model": args.model,
        "session_type_enabled": args.mpst_scope == "global",
        "session_type_scope": "global coordinator-mediated phase order" if args.mpst_scope == "global" else None,
        "session_type_max_retries": 2 if args.mpst_scope == "global" else 0,
        "workflow_config": "integrations/ChatDev1.0/CompanyConfig/MPSTPilot/ChatChainConfig.json",
        "status": status,
        "elapsed_seconds": elapsed,
        "project_path": str(project_path) if project_path else None,
        "output_dir": str(run_dir),
        "error": error,
    }
    (run_dir / "run_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps({
        "task_index": args.index, "condition": args.mpst_scope,
        "status": status, "elapsed_seconds": elapsed,
        "project_path": result["project_path"], "error": error,
    }, ensure_ascii=False), flush=True)
    return 0 if status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
