"""Evaluate ProgramDev artifacts with deterministic checks and an Ollama Cloud judge.

ProgramDev does not publish gold tests, so ``artifact_pass`` is an automated
proxy for the paper's human task-completion judgment, not a directly comparable
replacement for it.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, request


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "benchmarks" / "programdev"
DATASET = HERE / "programdev_dataset.json"
RUNS_ROOT = HERE / "runs"
SOURCE_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".java", ".c",
    ".cc", ".cpp", ".h", ".hpp", ".go", ".rs", ".php", ".rb", ".cs",
}
IGNORED_PARTS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--framework", choices=("chatdev", "metagpt", "all"), default="all")
    parser.add_argument(
        "--run-tag",
        default="",
        help="Optional experiment name under runs/<tag>/.",
    )
    parser.add_argument("--judge-model", default="glm-5.3-flash:cloud")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434/v1")
    parser.add_argument("--no-judge", action="store_true")
    parser.add_argument("--rerun-judge", action="store_true")
    parser.add_argument("--max-source-chars", type=int, default=60000)
    return parser.parse_args()


def find_workspace(run_dir: Path, result: dict[str, Any]) -> Path | None:
    chatdev_workspace = run_dir / "code_workspace"
    if chatdev_workspace.is_dir():
        return chatdev_workspace
    project_path = result.get("project_path")
    if project_path and Path(project_path).is_dir():
        return Path(project_path)
    return None


def source_files(workspace: Path) -> list[Path]:
    return sorted(
        path for path in walk_workspace_files(workspace) if path.suffix.lower() in SOURCE_SUFFIXES
    )


def walk_workspace_files(workspace: Path):
    """Walk artifacts without entering dependency trees or Windows junctions."""
    for directory, names, filenames in os.walk(workspace, topdown=True, followlinks=False):
        names[:] = [name for name in names if name not in IGNORED_PARTS]
        root = Path(directory)
        for filename in filenames:
            yield root / filename


def compile_python(files: list[Path]) -> dict[str, Any]:
    failures = []
    for path in files:
        if path.suffix.lower() != ".py":
            continue
        try:
            compile(path.read_text(encoding="utf-8-sig"), str(path), "exec")
        except Exception as exc:
            failures.append({"file": str(path), "error": f"{type(exc).__name__}: {exc}"})
    return {"checked": sum(path.suffix.lower() == ".py" for path in files), "failures": failures}


def check_project_integrity(workspace: Path, files: list[Path]) -> dict[str, Any]:
    issues: list[str] = []
    package_json_files = [path for path in walk_workspace_files(workspace) if path.name == "package.json"]
    frontend_sources = [path for path in files if path.suffix.lower() in {".jsx", ".tsx"}]
    if frontend_sources and not package_json_files:
        issues.append("JSX/TSX source exists but package.json is missing")
    for package_path in package_json_files:
        try:
            json.loads(package_path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            issues.append(f"invalid {package_path.relative_to(workspace)}: {exc}")

    root_main = workspace / "main.py"
    if root_main in files:
        try:
            imported = subprocess.run(
                [sys.executable, "-c", "import main"],
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                errors="replace",
            )
            if imported.returncode:
                issues.append("root main.py import failed: " + (imported.stderr or imported.stdout)[-2000:])
        except subprocess.TimeoutExpired:
            issues.append("root main.py import timed out")
    return {"passed": not issues, "issues": issues}


def run_pytest(workspace: Path, files: list[Path]) -> dict[str, Any]:
    test_files = [
        path for path in files
        if path.suffix.lower() == ".py" and (path.name.startswith("test_") or path.name.endswith("_test.py"))
    ]
    if not test_files:
        return {"available": False}
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=60,
            encoding="utf-8",
            errors="replace",
        )
        return {
            "available": True,
            "passed": completed.returncode == 0,
            "exit_code": completed.returncode,
            "output": (completed.stdout + completed.stderr)[-8000:],
        }
    except subprocess.TimeoutExpired:
        return {"available": True, "passed": False, "timed_out": True}


def source_bundle(workspace: Path, files: list[Path], max_chars: int) -> str:
    chunks: list[str] = []
    used = 0
    for path in files:
        try:
            content = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        relative = path.relative_to(workspace).as_posix()
        chunk = f"\n--- FILE: {relative} ---\n{content}\n"
        if used + len(chunk) > max_chars:
            remaining = max_chars - used
            if remaining > 200:
                chunks.append(chunk[:remaining])
            break
        chunks.append(chunk)
        used += len(chunk)
    return "".join(chunks)


def parse_json_response(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            raise
        value = json.loads(match.group(0))
    if not isinstance(value, dict):
        raise ValueError("judge response must be a JSON object")
    return value


def judge_artifact(
    description: str,
    bundle: str,
    model: str,
    base_url: str,
) -> dict[str, Any]:
    prompt = f"""You are a strict software acceptance reviewer. Assess only evidence in the files.
The benchmark requirement is:
{description}

Return exactly one JSON object with this schema:
{{
  "verdict": "pass" or "fail",
  "functional_completeness": number from 0 to 1,
  "executable_likelihood": number from 0 to 1,
  "implemented_requirements": [{{"requirement": string, "fulfilled": boolean, "evidence": string}}],
  "critical_issues": [string],
  "summary": string
}}
A pass requires all core requested features to be implemented, coherent, and likely executable. Do not
give credit for plans, manuals, TODOs, stubs, or claims without code evidence. Minor polish is not fatal.

Generated files:
{bundle}
"""
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "stream": False,
        }
    ).encode("utf-8")
    endpoint = base_url.rstrip("/") + "/chat/completions"
    req = request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "Authorization": "Bearer ollama"},
    )
    try:
        with request.urlopen(req, timeout=300) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"judge HTTP {exc.code}: {detail}") from exc
    content = payload["choices"][0]["message"]["content"]
    judged = parse_json_response(content)
    judged["model"] = model
    return judged


def evaluate_run(run_dir: Path, task: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    result_path = run_dir / "run_result.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    workspace = find_workspace(run_dir, result)
    evaluation_path = run_dir / "evaluation.json"
    previous = None
    if evaluation_path.exists():
        try:
            previous = json.loads(evaluation_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    files = source_files(workspace) if workspace else []
    compile_result = compile_python(files)
    integrity = check_project_integrity(workspace, files) if workspace else {
        "passed": False,
        "issues": ["workspace is missing"],
    }
    tests = run_pytest(workspace, files) if workspace else {"available": False}
    evaluation: dict[str, Any] = {
        "task_index": result["task_index"],
        "project_name": task["project_name"],
        "framework": result.get("framework"),
        "workflow_status": result.get("status"),
        "workspace": str(workspace) if workspace else None,
        "source_file_count": len(files),
        "python_compile": compile_result,
        "project_integrity": integrity,
        "self_tests": tests,
        "evaluated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    deterministic_ok = bool(files) and not compile_result["failures"] and integrity["passed"] and (
        not tests.get("available") or tests.get("passed", False)
    )
    if args.no_judge or not deterministic_ok:
        judge = previous.get("judge") if previous and not args.rerun_judge else None
    elif previous and previous.get("judge") and not args.rerun_judge:
        judge = previous["judge"]
    else:
        judge = judge_artifact(
            task["description"],
            source_bundle(workspace, files, args.max_source_chars),
            args.judge_model,
            args.base_url,
        )
    evaluation["judge"] = judge
    evaluation["artifact_pass"] = bool(
        deterministic_ok and judge and str(judge.get("verdict", "")).lower() == "pass"
    )
    evaluation_path.write_text(json.dumps(evaluation, indent=2, ensure_ascii=False), encoding="utf-8")
    return evaluation


def main() -> int:
    args = parse_args()
    if args.run_tag and not all(char.isalnum() or char in "._-" for char in args.run_tag):
        raise SystemExit("run-tag may contain only letters, numbers, dots, underscores, and hyphens")
    tasks = json.loads(DATASET.read_text(encoding="utf-8"))
    frameworks = ("chatdev", "metagpt") if args.framework == "all" else (args.framework,)
    run_root = RUNS_ROOT / args.run_tag if args.run_tag else RUNS_ROOT
    evaluations: list[dict[str, Any]] = []
    for framework in frameworks:
        framework_root = run_root / framework
        if not framework_root.exists():
            continue
        for result_path in sorted(framework_root.glob("*/run_result.json")):
            result = json.loads(result_path.read_text(encoding="utf-8"))
            index = int(result["task_index"])
            try:
                evaluation = evaluate_run(result_path.parent, tasks[index], args)
            except Exception as exc:
                evaluation = {
                    "task_index": index,
                    "project_name": tasks[index]["project_name"],
                    "framework": result.get("framework", framework),
                    "workflow_status": result.get("status"),
                    "artifact_pass": False,
                    "evaluation_error": f"{type(exc).__name__}: {exc}",
                }
            evaluations.append(evaluation)
            print(
                f"[{framework} {index:02d}] workflow={evaluation.get('workflow_status')} "
                f"artifact_pass={evaluation.get('artifact_pass')}",
                flush=True,
            )

    by_framework: dict[str, dict[str, Any]] = {}
    for framework in frameworks:
        items = [item for item in evaluations if str(item.get("framework", "")).lower() == framework]
        passed = sum(bool(item.get("artifact_pass")) for item in items)
        completed = sum(item.get("workflow_status") == "completed" for item in items)
        by_framework[framework] = {
            "evaluated": len(items),
            "artifact_passed": passed,
            "artifact_accuracy": passed / len(items) if items else None,
            "workflow_completed": completed,
            "workflow_completion_rate": completed / len(items) if items else None,
        }
    summary = {
        "method": "deterministic syntax/self-test gate plus Ollama Cloud LLM requirement audit",
        "run_tag": args.run_tag or None,
        "comparable_to_paper_human_accuracy": False,
        "judge_model": None if args.no_judge else args.judge_model,
        "frameworks": by_framework,
        "evaluations": evaluations,
    }
    tag_part = f"_{args.run_tag}" if args.run_tag else ""
    output_path = HERE / f"evaluation_summary{tag_part}.json"
    output_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(by_framework, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
