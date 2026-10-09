"""Contracts for the actual ChatDev 1.0 MPSTContent phase profile."""
from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

from .runtime import Violation
from .source_files import SourceExtractionError

ROOT = Path(__file__).resolve().parent.parent


class ContentViolation(RuntimeError):
    def __init__(self, contract, violations):
        self.contract = contract
        self.violations = violations
        super().__init__(json.dumps({"contract": contract, "violations": [asdict(v) for v in violations]}, ensure_ascii=False))


def fail(layer, rule, path, message, repair):
    return [Violation(layer, rule, path, message, repair)]


def snapshot(files):
    files = deepcopy(files)
    digests = {name: sha256(body.encode("utf-8")).hexdigest() for name, body in sorted(files.items())}
    identity = sha256(json.dumps(digests, sort_keys=True).encode()).hexdigest()
    return {"id": identity, "files": files, "digests": digests}


def compile_checks(files):
    for name, source in files.items():
        if name.endswith(".py"):
            try:
                tree = ast.parse(source, filename=name)
                compile(tree, name, "exec")  # also catches return outside function, etc.
            except (SyntaxError, ValueError) as error:
                return fail("C3", "python_compile", name, str(error), "Return syntactically valid Python source.")
    return []


def placeholders(files, selected=None):
    for name, source in files.items():
        if not name.endswith(".py") or (selected and name != selected):
            continue
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                body = node.body
                if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
                    body = body[1:]
                empty = not body or all(isinstance(n, ast.Pass) or (
                    isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and n.value.value is Ellipsis) for n in body)
                unimplemented = any(isinstance(n, ast.Raise) and n.exc is not None and (
                    isinstance(n.exc, ast.Name) and n.exc.id == "NotImplementedError" or
                    isinstance(n.exc, ast.Call) and isinstance(n.exc.func, ast.Name) and n.exc.func.id == "NotImplementedError") for n in body)
                if empty or unimplemented:
                    return fail("C2", "unimplemented_function", f"{name}:{node.lineno}",
                                f"Function {node.name} is a placeholder.", "Implement the function body.")
    return []


def startup_profile(files):
    """Select only supported, statically identifiable launch conventions."""
    trees = [ast.parse(body) for name, body in files.items() if name.endswith('.py')]
    imports_tk = any(isinstance(n, ast.Import) and any(a.name == 'tkinter' for a in n.names)
                     or isinstance(n, ast.ImportFrom) and n.module == 'tkinter'
                     for t in trees for n in ast.walk(t))
    has_loop = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                   and n.func.attr == 'mainloop' for t in trees for n in ast.walk(t))
    if imports_tk and has_loop:
        return 'tkinter_event_loop'
    required = []
    for node in ast.walk(ast.parse(files.get('main.py', ''))):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'add_argument':
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                name = node.args[0].value
                if not name.startswith('-') and not any(k.arg == 'nargs' for k in node.keywords):
                    required.append(name)
    imports_argparse = any(isinstance(n, ast.Import) and any(a.name == 'argparse' for a in n.names)
                           or isinstance(n, ast.ImportFrom) and n.module == 'argparse'
                           for t in trees for n in ast.walk(t))
    reads_text = any(isinstance(n, ast.Call) and (
        isinstance(n.func, ast.Attribute) and n.func.attr == 'read_text' or
        isinstance(n.func, ast.Name) and n.func.id == 'open' and any(k.arg == 'encoding' for k in n.keywords))
        for t in trees for n in ast.walk(t))
    if imports_argparse and reads_text and len(required) == 1 and required[0].lower() in {'file', 'filename', 'path', 'input_file', 'file_path'}:
        return 'text_file_cli'
    return 'process_exit'


def smoke_run(directory, files, timeout=3):
    """Trusted execution evidence, created by host code, never by agent payloads.

    This is a bounded startup check, not a unit-test or requirement-coverage claim.
    Only run generated code in an environment appropriate for its trust level.
    """
    source = snapshot(files)
    evidence = {"snapshot_id": source["id"], "source_digests": source["digests"],
                "kind": "startup_smoke", "command": [sys.executable, "-E", "main.py"],
                "timeout_seconds": timeout, "status": "inconclusive", "exit_code": None,
                "stdout": "", "stderr": ""}
    directory = Path(directory).resolve()
    def disk_matches():
        for name, body in files.items():
            target = (directory / name).resolve()
            try:
                if not target.is_relative_to(directory) or not target.is_file() or target.read_text(encoding="utf-8-sig") != body:
                    return False
            except (OSError, UnicodeError):
                return False
        return True
    if not disk_matches():
        evidence["stderr"] = "On-disk source differs from the candidate snapshot."
    else:
        if "main.py" not in files:
            evidence["stderr"] = "No main.py entry point in the source snapshot."
        else:
            try:
                options = {"creationflags": subprocess.CREATE_NO_WINDOW} if sys.platform == "win32" else {}
                with TemporaryDirectory(prefix='chatdev-startup-') as temporary:
                    profile = startup_profile(files)
                    evidence['profile'] = profile
                    record = Path(temporary) / 'probe.json'
                    if profile == 'tkinter_event_loop':
                        evidence['command'] = [sys.executable, '-E', str(ROOT / 'content_lab/startup_probe.py'),
                                               str(directory / 'main.py'), str(record)]
                    elif profile == 'text_file_cli':
                        fixture = 'level\nradar\nhello\nA man a plan a canal Panama\n'
                        path = Path(temporary) / 'input.txt'
                        path.write_text(fixture, encoding='utf-8')
                        evidence['fixture_sha256'] = sha256(fixture.encode()).hexdigest()
                        evidence['command'].append(str(path))
                    # An explicit EOF makes the host invocation deterministic: no inherited console/TTY.
                    result = subprocess.run(evidence["command"], cwd=directory, capture_output=True, input='',
                                            text=True, encoding="utf-8", errors="replace", timeout=timeout, **options)
                    evidence.update(status="passed" if result.returncode == 0 else "failed",
                                    exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
                    if profile == 'tkinter_event_loop':
                        observation = json.loads(record.read_text(encoding='utf-8')) if record.exists() else {}
                        evidence['observation'] = observation
                        if observation.get('callback_errors'):
                            evidence['stderr'] += '\n' + '\n'.join(observation['callback_errors'])
                        if result.returncode == 0 and not (observation.get('event_loop_observed') and observation.get('mapped_window')
                                and observation.get('widget_count', 0) > 0 and not observation.get('callback_errors')):
                            evidence['status'] = 'inconclusive'
                            evidence['stderr'] += '\nTk window/event-loop readiness was not observed.'
            except subprocess.TimeoutExpired as error:
                evidence["stderr"] = "Startup exceeded the time limit; success has not been established."
                evidence["stdout"] = (error.stdout or b"").decode("utf-8", errors="replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
            except OSError as error:
                evidence["stderr"] = str(error)
            if not disk_matches():
                evidence["status"] = "inconclusive"
                evidence["stderr"] += "\nSource changed during startup; execution cannot attest to the current snapshot."
    evidence["id"] = sha256(json.dumps(evidence, sort_keys=True).encode()).hexdigest()
    return evidence


def parse_json_response(text):
    # Transport formatting is not a semantic contract. Prefer an explicit final
    # envelope, otherwise require a single unambiguous complete object.
    text = text.strip()
    if text.startswith('<INFO>'):
        text = text[len('<INFO>'):].lstrip()
    # A terminal JSON fence is an explicit final payload; earlier reasoning or
    # drafts are outside that envelope and never delivered to downstream phases.
    fences = list(re.finditer(r'```json\s*\n(.*?)\n```', text, re.S))
    if fences and not text[fences[-1].end():].strip():
        try:
            value = json.loads(fences[-1].group(1))
        except ValueError:
            return None
        return value if isinstance(value, dict) else None
    decoder = json.JSONDecoder()
    # Raw JSON can follow an explicit prose conclusion. A terminal object must
    # start at a line/sentence boundary, not inside an unfinished parent object.
    for match in re.finditer(r'(?:^|\n|[.!?]\s*)(\{)', text):
        start = match.start(1)
        try:
            value, end = decoder.raw_decode(text, start)
        except ValueError:
            continue
        prefix = text[:start].rstrip()
        if end == len(text) and isinstance(value, dict) and (not prefix or prefix[-1] not in '{}[]:,'):
            return value
    objects = []
    position = 0
    while position < len(text):
        start = text.find('{', position)
        if start < 0:
            break
        try:
            value, end = decoder.raw_decode(text, start)
        except ValueError:
            return None  # never recover a nested object from a broken outer payload
        objects.append(value)
        position = end
    return objects[0] if len(objects) == 1 and isinstance(objects[0], dict) else None


def source_output(text, ctx):
    # Delegate extraction to the SAME parser that will apply files in ChatDev.
    from chatdev.codes import Codes
    try:
        extracted = Codes(text).codebooks
    except SourceExtractionError as error:
        return fail("C1", error.rule, "$", str(error),
                    "Return only final complete files, each as a standalone filename followed by a closed Python code fence. No drafts or analysis.")
    except Exception:
        extracted = {}
    if not extracted or not any(name.endswith(".py") for name in extracted):
        return fail("C1", "missing_source_files", "$", "No explicitly declared Python source files were delivered.",
                    "Stop analysis. Start with main.py on its own line followed by a fenced Python code block. Return compact complete executable files only.")
    for name in extracted:
        if Path(name).name != name or not re.fullmatch(r"[A-Za-z0-9_.-]+\.py", name):
            return fail("C1", "source_filename", name, "This profile accepts flat Python source files only.",
                        "Output Python filenames with no directory components.")
    merged = {**ctx["files"], **extracted}
    findings = compile_checks(merged)
    if findings:
        return findings
    if ctx["phase"] == "Coding" and "main.py" not in merged:
        return fail("C2", "entry_point", "$", "No main.py entry point.", "Provide main.py.")
    selected = ctx["phase_env"].get("unimplemented_file") if ctx["phase"] == "CodeComplete" else None
    if selected and selected not in extracted:
        return fail("C2", "requested_file", selected, "Requested completion file was not returned.", "Return the completed requested file.")
    return placeholders(merged, selected)


def content_nonempty(text, ctx):
    if not isinstance(text, str) or not text.strip():
        return fail("C1", "nonempty", "$", "Empty phase result.", "Return the required phase output.")
    return []


def language(text, ctx):
    if text.split("<INFO>")[-1].strip().rstrip(".").lower() != "python":
        return fail("C2", "python_profile", "$", "This profile implements Python code and evidence contracts.", "Return Python.")
    return []


def review(text, ctx):
    value = parse_json_response(text)
    if value is None or value.get("verdict") not in {"finished", "changes_requested"} or type(value.get("issues")) is not list:
        return fail("C1", "review_schema", "$", "Expected verdict and issues in a JSON object.",
                    'Return {"verdict":"finished|changes_requested","issues":[{"file":"main.py","line":1,"message":"..."}]}.')
    if not ctx["files"]:
        return fail("C3", "review_snapshot", "$", "No source to review.", "Review the host-provided source snapshot.")
    for issue in value["issues"]:
        if not isinstance(issue, dict) or type(issue.get("line")) is not int or type(issue.get("message")) is not str or not issue["message"].strip():
            return fail("C1", "issue_schema", "issues", "Malformed issue.", "Provide file, integer line, and nonempty message.")
        body = ctx["files"].get(issue.get("file"))
        if body is None or not 1 <= issue["line"] <= len(body.splitlines()):
            return fail("C3", "issue_location", "issues", "Issue does not identify a source line in the reviewed snapshot.", "Use an existing filename and source line.")
    if (value["verdict"] == "finished") != (len(value["issues"]) == 0):
        return fail("C2", "review_verdict", "verdict", "Verdict conflicts with issues.", "Use changes_requested for nonempty issues.")
    if value["verdict"] == "finished":
        return compile_checks(ctx["files"]) or placeholders(ctx["files"])
    return []


def modification(text, ctx):
    if text.split("<INFO>")[-1].strip().lower() == "finished":
        permitted = ctx["last_review"] and ctx["last_review"].get("verdict") == "finished" if ctx["phase"] == "CodeReviewModification" else ctx["evidence"] and ctx["evidence"]["status"] == "passed"
        if not permitted:
            return fail("C2", "premature_finished", "$", "Finished conflicts with required repairs.", "Return repaired source files.")
        return []
    return source_output(text, ctx)


def test_summary(text, ctx):
    value = parse_json_response(text)
    evidence = ctx["evidence"]
    if value is None or type(value.get("summary")) is not str or not value["summary"].strip():
        return fail("C1", "summary_schema", "$", "Expected a structured test summary.", "Return status, summary and test_run_id as JSON.")
    if not evidence or evidence["snapshot_id"] != snapshot(ctx["files"])["id"]:
        return fail("C3", "test_snapshot", "$", "No current execution evidence.", "Use host-generated current startup evidence.")
    if value.get("status") != evidence["status"] or value.get("test_run_id") != evidence["id"]:
        return fail("C2", "summary_evidence", "$", "Summary contradicts the startup execution record.", "Copy status and test_run_id from the host record.")
    return []


CHECKS = {"nonempty": content_nonempty, "python_language": language, "source_output": source_output,
          "review": review, "modification": modification, "test_summary": test_summary}


def startup_evidence(evidence, files, kind="startup_smoke"):
    expected = snapshot(files)
    if not isinstance(evidence, dict) or evidence.get("kind") != kind or evidence.get("status") not in {"passed", "failed", "inconclusive"}:
        return fail("C1", "startup_schema", "$", "Invalid startup execution record.", "Use evidence from the host execution adapter.")
    if evidence.get("snapshot_id") != expected["id"] or evidence.get("source_digests") != expected["digests"]:
        return fail("C3", "startup_version", "$", "Startup evidence belongs to another source snapshot.", "Execute the current source snapshot.")
    if (evidence["status"] == "passed" and evidence.get("exit_code") != 0) or (
            evidence["status"] == "failed" and (type(evidence.get("exit_code")) is not int or evidence["exit_code"] == 0)):
        return fail("C2", "startup_exit_status", "$", "Startup status contradicts the process exit code.", "Report the recorded process outcome.")
    if evidence.get('profile') == 'tkinter_event_loop' and evidence['status'] == 'passed':
        observed = evidence.get('observation', {})
        if not (observed.get('event_loop_observed') and observed.get('mapped_window')
                and observed.get('widget_count', 0) > 0 and not observed.get('callback_errors')):
            return fail('C3', 'gui_readiness', '$', 'No observed GUI startup readiness.', 'Use the host GUI probe.')
    body = {key: value for key, value in evidence.items() if key != "id"}
    if evidence.get("id") != sha256(json.dumps(body, sort_keys=True).encode()).hexdigest():
        return fail("C3", "startup_record_digest", "$", "Execution record was changed after creation.", "Use an unmodified host record.")
    return []


class ChatDevContracts:
    def __init__(self):
        self.registry = json.loads((ROOT / "chatdev-contracts.json").read_text(encoding="utf-8"))
        self.audit = []
        self.definitions = self.registry.get('contracts', {})
        for name, definition in self.definitions.items():
            if not definition.get('checks') or any(c not in CHECKS for c in definition['checks']):
                raise ValueError('Unknown contract checks: ' + name)
            attempts = definition.get('retry', {}).get('max_attempts')
            if type(attempts) is not int or attempts < 1:
                raise ValueError('Invalid retry policy: ' + name)
        if type(self.registry.get("max_attempts")) is not int or self.registry["max_attempts"] < 1:
            raise ValueError("Invalid ChatDev max_attempts")
        for item in self.registry["phases"].values():
            if not item["checks"] or any(c not in CHECKS for c in item["checks"]):
                raise ValueError("Unknown or empty ChatDev checks")

    def validate(self, phase, text, context, generation=None):
        item = self.registry["phases"].get(phase)
        if item is None:
            raise ValueError("Unmapped content phase: " + phase)
        return self._validate_item(phase, text, context, generation, item)

    def validate_contract(self, reference, text, context, generation=None, transition=None):
        if reference not in self.definitions:
            raise ValueError('Unknown protocol contract reference: ' + reference)
        definition = self.definitions[reference]
        declared_schema = (transition or {}).get('payload_schema')
        if declared_schema and declared_schema != definition['schema']:
            raise ValueError('Payload schema differs from contract: ' + reference)
        item = dict(definition, contract=reference)
        return self._validate_item(context.get('phase', 'protocol'), text, context,
                                   generation, item, transition)

    def _validate_item(self, phase, text, context, generation, item, transition=None):
        reasons = (generation or {}).get("termination_reasons", [])
        findings = fail("C1", "output_truncated", "$", "Model output reached its generation/context limit.",
                        "Output budget was exhausted. Omit analysis, architecture descriptions and drafts. Return a smaller complete implementation satisfying the task, with explicit filenames and closed code fences.") if any(r in {"length", "max_tokens_exceeded_by_camel"} for r in reasons) else []
        for name in ([] if findings else item["checks"]):
            try:
                findings = CHECKS[name](text, deepcopy(context))
            except Exception as error:
                findings = fail("runtime", name, "$", f"Validator raised {type(error).__name__}.", "Inspect the content validator.")
            if findings:
                break
        self.audit.append({"phase": phase, "contract": item["contract"], "snapshot_id": snapshot(context["files"])["id"],
                           "accepted": not findings, "violations": [asdict(v) for v in findings],
                           "candidate_sha256": sha256(text.encode("utf-8")).hexdigest(),
                           "termination_reasons": reasons,
                           "rejected_candidate": text if findings else None,
                           "interaction_id": (transition or {}).get('interaction_id'),
                           "trigger": 'projected_transition' if transition else 'legacy_direct_check'})
        if findings:
            raise ContentViolation(item["contract"], findings)


def startup_record(text, ctx):
    return startup_evidence(parse_json_response(text), ctx['files'])


def stage_exit(text, ctx):
    findings = compile_checks(ctx['files']) or startup_evidence(ctx.get('evidence'), ctx['files'])
    if findings:
        return findings
    if ctx['evidence']['status'] != 'passed':
        return fail('A', 'current_startup_passed', '$', 'Current startup did not pass.',
                    'Inspect host launch evidence and preserve required arguments and game behavior.')
    return []


CHECKS.update(startup_record=startup_record, stage_exit=stage_exit)
