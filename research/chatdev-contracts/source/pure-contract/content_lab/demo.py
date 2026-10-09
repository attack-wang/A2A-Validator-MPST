from __future__ import annotations

import argparse
import json
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from .code_review import CHECKS
from .runtime import Message, Runtime

ROOT = Path(__file__).resolve().parent.parent


def fixtures():
    files = {"calculator.py": "def add(a, b):\n    return a - b\n"}
    digests = {path: sha256(body.encode()).hexdigest() for path, body in files.items()}
    artifacts = {
        "source.v1": {"kind": "code_snapshot", "files": files, "digests": digests},
        "tests.v1": {"kind": "test_run", "snapshot_id": "source.v1", "source_digests": digests,
                     "outcomes": ["passed", "failed"], "exit_code": 1},
    }
    report = Message("Tester", "Reviewer", "testReport", {
        "snapshot_id": "source.v1", "test_run_id": "tests.v1",
        "passed": 1, "failed": 1, "total": 2, "status": "failed"})
    review = Message("Reviewer", "Coordinator", "reviewResult", {
        "snapshot_id": "source.v1", "test_run_id": "tests.v1", "verdict": "approve", "issues": []})
    return artifacts, report, review


def make_runtime(*, content_enabled=True, artifacts=None, checks=None, protocol=None):
    return Runtime(protocol or json.loads((ROOT / "protocol.json").read_text(encoding="utf-8")),
                   json.loads((ROOT / "contracts.json").read_text(encoding="utf-8")),
                   CHECKS if checks is None else checks,
                   fixtures()[0] if artifacts is None else artifacts,
                   content_enabled=content_enabled)


def run_demo():
    artifacts, report, review = fixtures()
    scenarios = []
    for enabled in (False, True):
        runtime = make_runtime(content_enabled=enabled, artifacts=artifacts)
        first = runtime.submit(report)
        before_artifacts = runtime.artifacts
        wrong = runtime.submit(review)
        scenario = {"mode": "content_contracts" if enabled else "protocol_only",
                    "test_report": first.to_dict(), "false_approval": wrong.to_dict(),
                    "artifacts_unchanged": before_artifacts == runtime.artifacts}
        if enabled:
            repaired = deepcopy(review.payload)
            repaired.update(verdict="reject", issues=[{
                "file": "calculator.py", "line": 2, "message": "add() subtracts instead of adding."}])
            scenario["repaired_review"] = runtime.submit(Message(
                review.sender, review.receiver, review.label, repaired)).to_dict()
        scenario["delivered_messages"] = len(runtime.history)
        scenario["final_state"] = runtime.state
        scenario["audit"] = runtime.audit
        scenarios.append(scenario)
    # Structurally valid, internally consistent lie. Only execution evidence exposes it.
    runtime = make_runtime()
    lie = deepcopy(report.payload)
    lie.update(passed=2, failed=0, status="passed")
    scenarios.append({"mode": "forged_test_counts", "decision": runtime.submit(
        Message(report.sender, report.receiver, report.label, lie)).to_dict()})
    stale = deepcopy(artifacts)
    stale["tests.v1"]["source_digests"] = {"calculator.py": "old-version"}
    runtime = make_runtime(artifacts=stale)
    scenarios.append({"mode": "stale_test_evidence", "decision": runtime.submit(report).to_dict()})
    return {"evidence_mode": "synthetic_fixture", "scenarios": scenarios}


def main():
    parser = argparse.ArgumentParser(description="Run isolated content-contract experiments (no API calls).")
    parser.add_argument("--output", type=Path, default=ROOT / "output" / "demo-results.json")
    args = parser.parse_args()
    result = run_demo()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for scenario in result["scenarios"]:
        decision = scenario.get("false_approval", scenario.get("decision"))
        rules = ", ".join(v["rule"] for v in decision["violations"]) or "none"
        print(f"{scenario['mode']}: accepted={decision['accepted']}, "
              f"state={decision['state_before']} -> {decision['state_after']}, violations={rules}")
        if "repaired_review" in scenario:
            print(f"  repaired_review: accepted={scenario['repaired_review']['accepted']}, "
                  f"state={scenario['final_state']}")
    print(f"Results: {args.output.resolve()}")


if __name__ == "__main__":
    main()
