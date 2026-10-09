"""Real 30-task batch, immutable input manifest, per-task outputs, resumable progress."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone, timedelta
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback

import evaluate

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CHATDEV = ROOT / "integrations" / "ChatDev1.0"
DATASET = HERE / "programdev_dataset.json"


def now():
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def save(path, payload):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def fingerprints():
    paths = [DATASET, Path(__file__), HERE / "evaluate.py", ROOT / "chatdev-contracts.json",
             ROOT / "content_lab/chatdev_contracts.py", ROOT / "content_lab/runtime.py",
             ROOT / "content_lab/source_files.py",
             ROOT / "content_lab/startup_probe.py",
             CHATDEV / "chatdev/content_guard.py", CHATDEV / "chatdev/phase.py",
             CHATDEV / "chatdev/chat_chain.py", CHATDEV / "chatdev/composed_phase.py",
             CHATDEV / "chatdev/chat_env.py", CHATDEV / "chatdev/codes.py",
             CHATDEV / "camel/agents/role_playing.py", CHATDEV / "camel/model_backend.py",
             CHATDEV / "camel/agents/chat_agent.py",
             CHATDEV / "protocol/mpst_content.gt"]
    paths += list((CHATDEV / "CompanyConfig/MPSTContent").glob("*.json"))
    return {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths}


def summarize(progress, batch_dir):
    runs = progress["runs"]
    rules = Counter(rule for run in runs for rule in run.get("violated_rules", []))
    summary = {"state": progress["state"], "planned": 30, "attempted": len(runs),
               "workflow_completed": sum(r["status"] == "completed" for r in runs),
               "workflow_failed": sum(r["status"] == "failed" for r in runs),
               "workflow_timeout": sum(r["status"] == "timeout" for r in runs),
               "artifact_passed": sum(r.get("artifact_pass") is True for r in runs),
               "evaluation_errors": sum(bool(r.get("evaluation_error")) for r in runs),
               "contract_rejection_events": sum(r.get("contract_rejections", 0) for r in runs),
               "violated_rules": dict(rules), "updated_at": now(),
               "measurement_note": "Workflow completion and software task-completion proxy are different metrics; no paired control in this batch."}
    save(batch_dir / "summary.json", summary)
    rows = ["# ChatDev 内容契约真实 30 题", "", f"状态：{summary['state']}；已运行：{len(runs)}/30。",
            f"流程完成：{summary['workflow_completed']}；失败：{summary['workflow_failed']}；超时：{summary['workflow_timeout']}。",
            f"自动工件评价通过：{summary['artifact_passed']}；评价异常：{summary['evaluation_errors']}。", "",
            "模型：glm-5.3-flash:cloud；配置：MPSTContent；每题限时：1500 秒。",
            "启动契约通过与完整题目功能通过分别统计。没有同批配对对照组。", "",
            "| 题号 | 题目 | 流程 | 契约拒绝次数 | 工件通过 | 原因/规则 |", "|---|---|---|---:|---|---|"]
    for run in runs:
        reason = ", ".join(run.get("violated_rules", [])) or (run.get("error") or "")
        rows.append(f"| {run['task_index']:02d} | {run['project_name']} | {run['status']} | {run.get('contract_rejections',0)} | {run.get('artifact_pass')} | {reason.replace('|','/').replace(chr(10),' ')[:240]} |")
    (batch_dir / "RESULTS.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def run_task(index, task, args, batch_dir):
    run_dir = batch_dir / "tasks" / f"{index:02d}_{task['project_name']}"
    if run_dir.exists():
        raise RuntimeError(f"Refusing to overwrite: {run_dir}")
    run_dir.mkdir(parents=True)
    name = f"PD{index:02d}{re.sub(r'[^A-Za-z0-9]', '', task['project_name'])}"
    warehouse = CHATDEV / "WareHouse"
    warehouse.mkdir(exist_ok=True)
    prefix = f"{name}_{args.batch_name}_"
    env = os.environ.copy()
    env.update(OPENAI_API_KEY=env.get("OPENAI_API_KEY") or "ollama", BASE_URL=args.base_url,
               CHATDEV_MODEL_NAME=args.model, CHATDEV_CONTEXT_LIMIT="32768", CHATDEV_MAX_TOKENS="8192",
               CHATDEV_REASONING_EFFORT="none", CHATDEV_CONTENT_ENABLED="true", CHATDEV_MPST_ENABLED="true",
               CHATDEV_MPST_SCOPE="global", MPST_A2A_ROOT=str(ROOT), PYTHONIOENCODING="utf-8",
               SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy")
    command = [sys.executable, "run.py", "--config", "MPSTContent", "--org", args.batch_name,
               "--task", task["description"], "--name", name, "--model", "GPT_4O"]
    start = time.monotonic()
    status, error = "failed", None
    with (run_dir / "console.log").open("w", encoding="utf-8") as output:
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        process = subprocess.Popen(command, cwd=CHATDEV, env=env, stdout=output,
                                   stderr=subprocess.STDOUT, creationflags=flags)
        try:
            code = process.wait(timeout=args.timeout)
            status = "completed" if code == 0 else "failed"
            error = f"exit code {code}" if code else None
        except subprocess.TimeoutExpired:
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, creationflags=flags)
            else:
                process.kill()
            process.wait()
            status, error = "timeout", f"exceeded {args.timeout} seconds"
    created = sorted((p for p in warehouse.glob(prefix + "*") if p.is_dir()), key=lambda p: p.stat().st_mtime)
    project = created[-1] if created else None
    audit_path = project / "content-contract-audit.json" if project else None
    audit = json.loads(audit_path.read_text(encoding="utf-8")) if audit_path and audit_path.exists() else {}
    failures = [c for c in audit.get("checks", []) if c.get("accepted") is False]
    violated_rules = [v["rule"] for c in failures for v in c.get("violations", [])]
    if any(c.get("contract") == "chatdev.stage_exit.v1" for c in failures) and 'current_startup_passed' not in violated_rules:
        violated_rules.append("current_startup_passed")
    if audit:
        save(run_dir / "content-contract-audit.json", audit)
    console = (run_dir / "console.log").read_text(encoding="utf-8", errors="replace")
    failure_type = ("timeout" if status == "timeout" else "content_contract" if "ContentViolation:" in console
                    else "runtime_error" if status == "failed" else None)
    result = {"task_index": index, "project_name": task["project_name"], "description": task["description"],
              "framework": "ChatDev1.0", "model": args.model, "content_contracts_enabled": True,
              "session_type_enabled": True, "status": status, "error": error,
              "failure_type": failure_type,
              "project_path": str(project) if project else None, "elapsed_seconds": round(time.monotonic()-start, 3),
              "contract_rejections": len(failures), "violated_rules": violated_rules,
              "last_diagnostic": console[-5000:] if status != "completed" else None}
    save(run_dir / "run_result.json", result)
    evaluation_error, evaluation = None, None
    try:
        options = argparse.Namespace(no_judge=False, rerun_judge=False, max_source_chars=60000,
                                     judge_model=args.judge_model, base_url=args.base_url)
        evaluation = evaluate.evaluate_run(run_dir, task, options)
    except Exception as exc:
        evaluation_error = f"{type(exc).__name__}: {exc}"
        save(run_dir / "evaluation-error.json", {"error": evaluation_error, "traceback": traceback.format_exc()})
    result.update(artifact_pass=evaluation.get("artifact_pass") if evaluation else None,
                  evaluation_error=evaluation_error, result_path=str(run_dir / "run_result.json"))
    save(run_dir / "run_result.json", result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-name", required=True)
    parser.add_argument("--timeout", type=int, default=1500)
    parser.add_argument("--model", default="glm-5.3-flash:cloud")
    parser.add_argument("--judge-model", default="gpt-oss:120b-cloud")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434/v1")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.batch_name):
        parser.error("Invalid batch name")
    tasks = json.loads(DATASET.read_text(encoding="utf-8"))
    if len(tasks) != 30:
        raise RuntimeError("Expected exactly 30 tasks")
    batch_dir = HERE / "runs" / args.batch_name
    hashes = fingerprints()
    if args.resume:
        manifest = json.loads((batch_dir / "manifest.json").read_text(encoding="utf-8"))
        if manifest["sha256"] != hashes or manifest["model"] != args.model:
            raise RuntimeError("Cannot resume after source/config/model changed")
        progress = json.loads((batch_dir / "progress.json").read_text(encoding="utf-8"))
        progress.update(state="running", pid=os.getpid())
    else:
        batch_dir.mkdir(parents=True, exist_ok=False)
        save(batch_dir / "manifest.json", {"started_at": now(), "model": args.model, "judge_model": args.judge_model,
             "dataset_size": 30, "timeout_seconds": args.timeout, "sha256": hashes,
             "python": sys.executable, "profile": "MPSTContent", "serial": True,
             "generation_settings": {"max_tokens": 8192, "context_limit": 32768, "reasoning_effort": "none"},
             "dataset": tasks})
        progress = {"state": "running", "pid": os.getpid(), "started_at": now(), "current": None, "runs": []}
    save(batch_dir / "progress.json", progress)
    completed = {r["task_index"] for r in progress["runs"]}
    try:
        for index, task in enumerate(tasks):
            if index in completed:
                continue
            if fingerprints() != hashes:
                raise RuntimeError("Source changed during batch; stopped to preserve comparability")
            progress["current"] = {"task_index": index, "project_name": task["project_name"], "started_at": now()}
            save(batch_dir / "progress.json", progress)
            print(f"[{index+1}/30] {task['project_name']}", flush=True)
            result = run_task(index, task, args, batch_dir)
            progress["runs"].append(result)
            progress["current"] = None
            save(batch_dir / "progress.json", progress)
            summarize(progress, batch_dir)
            print(f"  status={result['status']} rejections={result['contract_rejections']} artifact_pass={result['artifact_pass']}", flush=True)
        progress["state"] = "complete"
    except Exception:
        progress.update(state="stopped", fatal_error=traceback.format_exc())
        print(progress["fatal_error"], file=sys.stderr, flush=True)
    finally:
        progress.update(updated_at=now(), current=None)
        save(batch_dir / "progress.json", progress)
        summarize(progress, batch_dir)
    return 0 if progress["state"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
