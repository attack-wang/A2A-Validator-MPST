"""Code-review domain plugin. Evidence is supplied by a trusted adapter.

The demo adapter uses fixtures. It does not prove that real tests were executed.
"""
from __future__ import annotations

from hashlib import sha256

from .runtime import Violation


def problem(layer, rule, path, message, repair):
    return [Violation(layer, rule, path, message, repair)]


def test_schema(p, ctx):
    required = {"snapshot_id": str, "test_run_id": str, "passed": int,
                "failed": int, "total": int, "status": str}
    for field, kind in required.items():
        if type(p.get(field)) is not kind:
            return problem("C1", "test_schema", field, f"Required {kind.__name__} field.",
                           "Provide all test-report fields with exact types.")
    if p["status"] not in {"passed", "failed"}:
        return problem("C1", "test_schema", "status", "Unsupported test status.", "Use passed or failed.")
    return []


def test_counts(p, ctx):
    if min(p["passed"], p["failed"]) < 0 or p["total"] <= 0 or p["total"] != p["passed"] + p["failed"]:
        return problem("C2", "test_counts", "total", "Test counts are inconsistent or empty.",
                       "Report nonnegative counts from a nonempty test run.")
    if p["status"] != ("passed" if p["failed"] == 0 else "failed"):
        return problem("C2", "test_status", "status", "Status disagrees with failure count.",
                       "Set status to failed when failed > 0.")
    return []


def source_snapshot(snapshot_id, ctx):
    snapshot = ctx["artifacts"].get(snapshot_id)
    if not isinstance(snapshot, dict) or snapshot.get("kind") != "code_snapshot":
        return None
    files = snapshot.get("files")
    if not isinstance(files, dict) or not files:
        return None
    if any(not isinstance(path, str) or not isinstance(body, str) for path, body in files.items()):
        return None
    if snapshot.get("digests") != {path: sha256(body.encode()).hexdigest() for path, body in files.items()}:
        return None
    return snapshot


def test_evidence(p, ctx):
    source = source_snapshot(p["snapshot_id"], ctx)
    run = ctx["artifacts"].get(p["test_run_id"])
    if source is None or not isinstance(run, dict) or run.get("kind") != "test_run":
        return problem("C3", "test_evidence", "test_run_id", "Missing or invalid source/test evidence.",
                       "Reference a trusted test run and a source snapshot with valid digests.")
    if run.get("snapshot_id") != p["snapshot_id"] or run.get("source_digests") != source["digests"]:
        return problem("C3", "test_version", "snapshot_id", "Tests belong to another source version.",
                       "Run tests against the referenced source snapshot.")
    outcomes = run.get("outcomes")
    if not isinstance(outcomes, list) or not outcomes or any(v not in {"passed", "failed"} for v in outcomes):
        return problem("C3", "test_evidence", "outcomes", "No valid test outcomes.", "Supply trusted outcomes.")
    actual = {"passed": outcomes.count("passed"), "failed": outcomes.count("failed"), "total": len(outcomes)}
    if any(p[field] != value for field, value in actual.items()) or run.get("exit_code") != (0 if actual["failed"] == 0 else 1):
        return problem("C3", "test_evidence", "passed", "Report disagrees with recorded test execution.",
                       "Use counts and exit status from the referenced test run.")
    return []


def review_schema(p, ctx):
    for field, kind in {"snapshot_id": str, "test_run_id": str, "verdict": str, "issues": list}.items():
        if type(p.get(field)) is not kind:
            return problem("C1", "review_schema", field, f"Required {kind.__name__} field.", "Fix the review schema.")
    if p["verdict"] not in {"approve", "reject"}:
        return problem("C1", "review_schema", "verdict", "Unknown verdict.", "Use approve or reject.")
    for i, issue in enumerate(p["issues"]):
        if not isinstance(issue, dict) or type(issue.get("file")) is not str or type(issue.get("line")) is not int or type(issue.get("message")) is not str or not issue["message"].strip():
            return problem("C1", "issue_location", f"issues[{i}]", "Issue requires file, integer line and message.",
                           "Provide an actionable issue location and description.")
    return []


def review_consistency(p, ctx):
    reports = [m.payload for m in ctx["history"] if m.label == "testReport"]
    if not reports:
        return problem("C2", "test_history", "$", "No accepted test report.", "Deliver a verified testReport first.")
    report = reports[-1]
    if p["snapshot_id"] != report["snapshot_id"] or p["test_run_id"] != report["test_run_id"]:
        return problem("C2", "history_version", "test_run_id", "Review references different evidence than the accepted report.",
                       "Use the accepted report's snapshot and test-run identifiers.")
    if p["verdict"] == "approve" and (p["issues"] or report["failed"] > 0):
        return problem("C2", "verdict_consistent", "verdict", "Approval conflicts with open issues or failed tests.",
                       "Reject the review or supply repaired code and a new verified test session.")
    return []


def review_evidence(p, ctx):
    source = source_snapshot(p["snapshot_id"], ctx)
    if source is None:
        return problem("C3", "code_snapshot", "snapshot_id", "Missing or invalid source snapshot.", "Supply trusted source evidence.")
    for i, issue in enumerate(p["issues"]):
        body = source["files"].get(issue["file"])
        if body is None or not 1 <= issue["line"] <= len(body.splitlines()):
            return problem("C3", "issue_location", f"issues[{i}]", "Issue location does not exist in the snapshot.",
                           "Reference an existing file and one-based source line.")
    return []


CHECKS = {fn.__name__: fn for fn in (test_schema, test_counts, test_evidence,
                                   review_schema, review_consistency, review_evidence)}
