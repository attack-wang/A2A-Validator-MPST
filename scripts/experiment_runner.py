"""Run paired A2A experiments and capture application-level communication.

The runner drives the same HTTP endpoints as the Mesop UI. It can start all
configured services twice (validation on/off), create a fresh conversation for
every run, wait for the Host to finish, and export messages, internal ADK
events, tasks, process-log slices, and summary tables.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import platform
import re
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid

from collections import Counter
from pathlib import Path
from typing import Any, Iterable


MISSING = object()
TOOL_LEAK_RE = re.compile(
    r"(?:Tool\s*Calls?\s*:|"
    r"[\"']name[\"']\s*:\s*[\"'](?:send_message|finalize_protocol)[\"'])",
    re.IGNORECASE,
)
ERROR_FINAL_RE = re.compile(
    r"^\s*(?:处理请求时发生错误|"
    r"Host\s*模型连续返回空内容|"
    r"Error\s+processing\s+request\s*:|"
    r"Execution\s+error\s*:|"
    r"(?:###\s*User:\s*)?\{\s*[\"']status[\"']\s*:\s*[\"']error[\"'])",
    re.IGNORECASE,
)
A2A_TRACE_RE = re.compile(r"\[A2A COMMUNICATION\]\s+(\{.*\})\s*$")


def json_dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )


def csv_dump(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def safe_name(value: str) -> str:
    normalized = re.sub(r"[^0-9A-Za-z_.-]+", "-", value.strip())
    return normalized.strip("-") or "run"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _command_version(command: list[str], cwd: Path) -> str:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def reproducibility_metadata(project_root: Path) -> dict[str, Any]:
    """Capture non-secret runtime provenance alongside every experiment."""
    commit = _command_version(["git", "rev-parse", "HEAD"], project_root)
    status = _command_version(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        project_root,
    )
    return {
        "captured_at": utc_now(),
        "git_commit": commit,
        "git_tracked_worktree_dirty": bool(status),
        "python": sys.version,
        "platform": platform.platform(),
        "uv": _command_version(["uv", "--version"], project_root),
    }


def merge_config(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge a small experiment override onto a base config."""
    merged = dict(base)
    for key, value in override.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = merge_config(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_experiment_config(config_path: Path) -> dict[str, Any]:
    """Load a JSON config, optionally inheriting from another JSON file."""
    data = json.loads(config_path.read_text(encoding="utf-8"))
    parent = data.pop("extends", None)
    if not parent:
        return data
    parent_path = (config_path.parent / str(parent)).resolve()
    if parent_path == config_path.resolve():
        raise ValueError("Experiment config cannot extend itself")
    return merge_config(load_experiment_config(parent_path), data)


def resolve_dynamic_prompt(prompt: dict[str, Any], today: dt.date) -> dict[str, str]:
    """Resolve relative dates once so paired modes receive byte-identical text."""
    prompt_id = str(prompt["id"])
    if "text" in prompt:
        return {"id": prompt_id, "text": str(prompt["text"])}

    template = str(prompt["template"])
    variables = dict(prompt.get("variables", {}))
    if "start_offset_days" in prompt:
        start = today + dt.timedelta(days=int(prompt["start_offset_days"]))
        variables["start_date"] = start.isoformat()
        duration = int(prompt.get("duration_days", 2))
        variables["end_date"] = (
            start + dt.timedelta(days=max(duration - 1, 0))
        ).isoformat()
    return {"id": prompt_id, "text": template.format(**variables)}


def part_root(part: Any) -> dict[str, Any]:
    if not isinstance(part, dict):
        return {}
    root = part.get("root", part)
    return root if isinstance(root, dict) else {}


def part_content(part: Any) -> tuple[str, str]:
    root = part_root(part)
    kind = str(root.get("kind", "unknown"))
    if kind == "text":
        return kind, str(root.get("text", ""))
    if kind == "data":
        return kind, json.dumps(
            root.get("data"), ensure_ascii=False, default=str
        )
    if kind == "file":
        return kind, json.dumps(
            root.get("file"), ensure_ascii=False, default=str
        )
    return kind, json.dumps(root, ensure_ascii=False, default=str)


def message_visible_text(message: Any) -> str:
    if not isinstance(message, dict):
        return ""
    chunks = []
    for part in message.get("parts") or []:
        kind, content = part_content(part)
        if kind in {"text", "data"} and content.strip():
            chunks.append(content.strip())
    return "\n".join(chunks)


def trace_payload_text(record: dict[str, Any]) -> str:
    """Extract the visible request text from one captured A2A trace record."""
    payload = record.get("payload")
    if not isinstance(payload, dict):
        return ""
    return message_visible_text(payload)


def final_output_checklist(
    final_text: str,
    *,
    used_agents: set[str],
    usable: bool,
    expected_dates: tuple[str, str] | None = None,
) -> dict[str, bool]:
    """Score the six observable final-output requirements for travel plans."""
    if not usable:
        return {
            "output_transport_complete": False,
            "output_hotel_complete": False,
            "output_ticket_complete": False,
            "output_weather_adapted": False,
            "output_daily_routes_complete": False,
            "output_budget_complete": False,
        }

    if expected_dates is None:
        dates_in_text = re.findall(r"\d{4}-\d{2}-\d{2}", final_text)
        expected_dates = (
            (dates_in_text[0], dates_in_text[-1])
            if dates_in_text
            else ("2026-08-10", "2026-08-13")
        )

    def contains_date(iso_date: str) -> bool:
        try:
            parsed = dt.date.fromisoformat(iso_date)
        except ValueError:
            return iso_date in final_text
        variants = (
            parsed.isoformat(),
            f"{parsed.year}年{parsed.month}月{parsed.day}日",
            f"{parsed.month}月{parsed.day}日",
        )
        compact = re.sub(r"\s+", "", final_text)
        return any(value in compact for value in variants)

    outbound_date = contains_date(expected_dates[0])
    return_date = contains_date(expected_dates[1])
    vehicle_number = bool(
        re.search(
            r"(?<![A-Z0-9])(?:G|D|C|K|T|Z)\d{1,4}(?![A-Z0-9])"
            r"|(?<![A-Z0-9])[A-Z]{2}\d{3,4}(?![A-Z0-9])",
            final_text,
        )
    )
    outbound_and_return = bool(
        re.search(r"去程|往返", final_text)
        and re.search(r"返程|往返", final_text)
    )
    hotel_complete = bool(
        re.search(r"酒店|宾馆|饭店", final_text)
        and re.search(r"3\s*晚|三\s*晚", final_text)
    )
    sight_words = (
        "故宫", "国家博物馆", "首都博物馆", "颐和园", "圆明园",
        "长城", "慕田峪", "雍和宫", "中国美术馆", "天坛", "景山",
        "前门", "鸟巢", "王府井", "孔庙", "国子监",
    )
    ticket_complete = bool(
        "门票" in final_text
        and sum(word in final_text for word in sight_words) >= 3
        and re.search(r"预约|购票|预订|出票|购买", final_text)
    )
    weather_adapted = bool(
        re.search(r"天气|降雨|下雨|毛毛雨|雷暴|降雪", final_text)
        and "室内" in final_text
        and "户外" in final_text
    )
    daily_routes_complete = bool(
        re.search(r"地铁|公交|打车|公共交通", final_text)
        and re.search(r"换乘|路线|起点|终点|出发", final_text)
        and re.search(r"费用|价格|元", final_text)
    )
    budget_complete = bool(
        "Budget Agent" in used_agents
        and re.search(r"总费用|总计|合计", final_text)
        and re.search(r"人均|每人", final_text)
        and re.search(r"交通", final_text)
        and re.search(r"住宿|酒店", final_text)
        and re.search(r"门票", final_text)
    )
    return {
        "output_transport_complete": (
            outbound_date
            and return_date
            and vehicle_number
            and outbound_and_return
        ),
        "output_hotel_complete": hotel_complete,
        "output_ticket_complete": ticket_complete,
        "output_weather_adapted": weather_adapted,
        "output_daily_routes_complete": daily_routes_complete,
        "output_budget_complete": budget_complete,
    }


def message_role(message: Any) -> str:
    if not isinstance(message, dict):
        return ""
    role = message.get("role", "")
    if isinstance(role, dict):
        return str(role.get("value") or role.get("name") or role)
    return str(role)


def message_id(message: Any) -> str:
    if not isinstance(message, dict):
        return ""
    return str(message.get("message_id") or message.get("messageId") or "")


def context_id(message: Any) -> str:
    if not isinstance(message, dict):
        return ""
    return str(message.get("context_id") or message.get("contextId") or "")


def task_id(message: Any) -> str:
    if not isinstance(message, dict):
        return ""
    return str(message.get("task_id") or message.get("taskId") or "")


def iter_mappings(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for nested in value.values():
            yield from iter_mappings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_mappings(nested)


def event_tool_calls(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    seen: set[str] = set()
    for event in events:
        content = event.get("content") or {}
        for part in content.get("parts") or []:
            root = part_root(part)
            candidates: list[Any] = []
            if root.get("kind") == "data":
                candidates.append(root.get("data"))
            elif root.get("kind") == "text":
                text = root.get("text")
                if isinstance(text, str):
                    try:
                        candidates.append(json.loads(text))
                    except json.JSONDecodeError:
                        continue
            for candidate in candidates:
                for mapping in iter_mappings(candidate):
                    name = mapping.get("name")
                    args = mapping.get("args", mapping.get("arguments"))
                    if not isinstance(name, str) or not isinstance(args, dict):
                        continue
                    fingerprint = json.dumps(
                        [event.get("id"), name, args],
                        ensure_ascii=False,
                        sort_keys=True,
                        default=str,
                    )
                    if fingerprint in seen:
                        continue
                    seen.add(fingerprint)
                    calls.append(
                        {
                            "event_id": event.get("id", ""),
                            "timestamp": event.get("timestamp", ""),
                            "name": name,
                            "arguments": args,
                        }
                    )
    return calls


def parse_a2a_trace(log_text: str) -> list[dict[str, Any]]:
    records = []
    for line in log_text.splitlines():
        match = A2A_TRACE_RE.search(line)
        if not match:
            continue
        try:
            record = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            records.append(record)
    return records


def task_state(task: dict[str, Any]) -> str:
    status = task.get("status") or {}
    state = status.get("state", "") if isinstance(status, dict) else ""
    return str(state).split(".")[-1].lower()


def communication_rows(
    run_id: str,
    messages: list[dict[str, Any]],
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sequence = 0
    for event in sorted(events, key=lambda x: float(x.get("timestamp") or 0)):
        content = event.get("content") or {}
        for index, part in enumerate(content.get("parts") or []):
            sequence += 1
            kind, value = part_content(part)
            rows.append(
                {
                    "run_id": run_id,
                    "sequence": sequence,
                    "source": "event",
                    "timestamp": event.get("timestamp", ""),
                    "actor": event.get("actor", ""),
                    "role": message_role(content),
                    "message_id": message_id(content),
                    "context_id": context_id(content),
                    "task_id": task_id(content),
                    "part_index": index,
                    "part_kind": kind,
                    "content": value,
                }
            )

    event_message_ids = {
        message_id(event.get("content") or {}) for event in events
    }
    for message in messages:
        if message_id(message) in event_message_ids:
            continue
        for index, part in enumerate(message.get("parts") or []):
            sequence += 1
            kind, value = part_content(part)
            rows.append(
                {
                    "run_id": run_id,
                    "sequence": sequence,
                    "source": "conversation",
                    "timestamp": "",
                    "actor": "user" if message_role(message) == "user" else "host",
                    "role": message_role(message),
                    "message_id": message_id(message),
                    "context_id": context_id(message),
                    "task_id": task_id(message),
                    "part_index": index,
                    "part_kind": kind,
                    "content": value,
                }
            )
    return rows


class ApiClient:
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def post(
        self,
        path: str,
        method: str,
        params: Any = MISSING,
        *,
        attempts: int = 1,
    ) -> Any:
        payload: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": uuid.uuid4().hex,
            "method": method,
        }
        if params is not MISSING:
            payload["params"] = params
        request = urllib.request.Request(
            self.base_url + path,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        last_error: Exception | None = None
        for attempt in range(attempts):
            try:
                with urllib.request.urlopen(
                    request, timeout=self.timeout
                ) as response:
                    body = json.loads(response.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as exc:
                error_body = exc.read().decode("utf-8", errors="replace")
                last_error = RuntimeError(
                    f"{path} returned HTTP {exc.code}: {error_body}"
                )
                if exc.code < 500 or attempt + 1 >= attempts:
                    raise last_error from exc
            except (
                urllib.error.URLError,
                ConnectionError,
                TimeoutError,
                OSError,
            ) as exc:
                last_error = exc
                if attempt + 1 >= attempts:
                    raise RuntimeError(
                        f"{path} failed after {attempts} attempts: {exc}"
                    ) from exc
            time.sleep(min(0.5 * (2**attempt), 3))
        else:
            raise RuntimeError(f"{path} failed: {last_error}")
        if body.get("error"):
            raise RuntimeError(f"{method} failed: {body['error']}")
        return body.get("result")

    def create_conversation(self) -> dict[str, Any]:
        return self.post(
            "/conversation/create", "conversation/create"
        ) or {}

    def list_messages(self, conversation: str) -> list[dict[str, Any]]:
        return self.post(
            "/message/list", "message/list", conversation, attempts=4
        ) or []

    def list_events(self) -> list[dict[str, Any]]:
        return self.post("/events/get", "events/get", attempts=4) or []

    def list_tasks(self) -> list[dict[str, Any]]:
        return self.post("/task/list", "task/list", attempts=4) or []

    def pending(self) -> list[list[str]]:
        return self.post(
            "/message/pending", "message/pending", attempts=4
        ) or []

    def list_agents(self) -> list[dict[str, Any]]:
        return self.post("/agent/list", "agent/list", attempts=4) or []

    def register_agent(self, url: str) -> None:
        self.post("/agent/register", "agent/register", url)

    def send_message(self, conversation: str, prompt: str) -> str:
        request_id = str(uuid.uuid4())
        params = {
            "message_id": request_id,
            "context_id": conversation,
            "role": "user",
            "parts": [{"kind": "text", "text": prompt}],
        }
        result = self.post("/message/send", "message/send", params) or {}
        return str(
            result.get("message_id")
            or result.get("messageId")
            or request_id
        )


class ServiceGroup:
    def __init__(
        self,
        project_root: Path,
        services: list[dict[str, Any]],
        mode_dir: Path,
        explicit_env: dict[str, str],
    ):
        self.project_root = project_root
        self.services = services
        self.mode_dir = mode_dir
        self.explicit_env = explicit_env
        self.processes: list[tuple[dict[str, Any], subprocess.Popen[Any], Any]] = []
        self.log_paths: dict[str, Path] = {}

    @staticmethod
    def _port_open(port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.25)
            return sock.connect_ex(("127.0.0.1", port)) == 0

    def ensure_ports_free(self) -> None:
        occupied = [
            f"{service['name']}:{service['port']}"
            for service in self.services
            if self._port_open(int(service["port"]))
        ]
        if occupied:
            joined = ", ".join(occupied)
            raise RuntimeError(
                "Configured ports are already occupied: "
                f"{joined}. Stop the manually started services, or use "
                "--reuse-services for a single mode."
            )

    def start_one(self, service: dict[str, Any]) -> None:
        command = [str(item) for item in service["command"]]
        if (
            len(command) >= 2
            and command[0] == "uv"
            and command[1] == "run"
            and "--frozen" not in command
        ):
            command.insert(2, "--frozen")
        if shutil.which(command[0]) is None:
            raise RuntimeError(f"Executable not found: {command[0]}")
        cwd = (self.project_root / service["cwd"]).resolve()
        log_path = self.mode_dir / "_service_logs" / f"{safe_name(service['name'])}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        stream = log_path.open("wb")
        env = os.environ.copy()
        env.update(self.explicit_env)
        env.update({str(k): str(v) for k, v in service.get("env", {}).items()})
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        creationflags = 0
        start_new_session = os.name != "nt"
        if os.name == "nt":
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=stream,
            stderr=subprocess.STDOUT,
            creationflags=creationflags,
            start_new_session=start_new_session,
        )
        self.processes.append((service, process, stream))
        self.log_paths[str(service["name"])] = log_path

    @staticmethod
    def wait_url(url: str, timeout: float) -> None:
        deadline = time.monotonic() + timeout
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            try:
                with urllib.request.urlopen(url, timeout=3) as response:
                    if response.status < 500:
                        return
            except Exception as exc:  # readiness must tolerate connection errors
                last_error = exc
            time.sleep(0.5)
        raise TimeoutError(f"Service did not become ready: {url}; {last_error}")

    def start(self, startup_timeout: float) -> None:
        self.ensure_ports_free()
        remotes = [s for s in self.services if s.get("role") == "remote"]
        hosts = [s for s in self.services if s.get("role") == "host"]
        try:
            for service in remotes:
                self.start_one(service)
            for service in remotes:
                readiness = service.get(
                    "readiness_url",
                    str(service["url"]).rstrip("/")
                    + "/.well-known/agent-card.json",
                )
                self.wait_url(str(readiness), startup_timeout)
            for service in hosts:
                self.start_one(service)
            for service in hosts:
                self.wait_url(str(service["url"]), startup_timeout)
        except Exception:
            self.stop()
            raise

    def log_offsets(self) -> dict[str, int]:
        offsets = {}
        for name, path in self.log_paths.items():
            offsets[name] = path.stat().st_size if path.exists() else 0
        return offsets

    def copy_log_slices(self, offsets: dict[str, int], target: Path) -> str:
        target.mkdir(parents=True, exist_ok=True)
        combined: list[str] = []
        for name, path in self.log_paths.items():
            if not path.exists():
                continue
            with path.open("rb") as stream:
                stream.seek(offsets.get(name, 0))
                data = stream.read()
            text = data.decode("utf-8", errors="replace")
            (target / f"{safe_name(name)}.log").write_text(text, encoding="utf-8")
            if text:
                combined.append(f"===== {name} =====\n{text}")
        return "\n".join(combined)

    def stop(self) -> None:
        for _, process, _ in reversed(self.processes):
            if process.poll() is not None:
                continue
            if os.name == "nt":
                subprocess.run(
                    ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            else:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
        for _, process, stream in self.processes:
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
            stream.close()
        self.processes.clear()

        deadline = time.monotonic() + 30
        occupied: list[str] = []
        while time.monotonic() < deadline:
            occupied = [
                f"{service['name']}:{service['port']}"
                for service in self.services
                if self._port_open(int(service["port"]))
            ]
            if not occupied:
                return
            time.sleep(0.25)
        print(
            "Warning: service ports were still occupied after shutdown: "
            + ", ".join(occupied),
            file=sys.stderr,
        )


class ExperimentRunner:
    def __init__(
        self,
        config_path: Path,
        *,
        mode_choice: str = "both",
        repetitions: int | None = None,
        reuse_services: bool = False,
        output_root: Path | None = None,
        resume_dir: Path | None = None,
    ):
        self.config_path = config_path.resolve()
        self.config = load_experiment_config(self.config_path)
        self.project_root = (
            self.config_path.parent / self.config.get("project_root", ".")
        ).resolve()
        configured_output = self.config.get("output_root", "experiments/results")
        self.output_root = (
            output_root.resolve()
            if output_root
            else (self.project_root / configured_output).resolve()
        )
        self.mode_choice = mode_choice
        self.repetitions = int(
            repetitions
            if repetitions is not None
            else self.config.get("repetitions", 1)
        )
        self.reuse_services = reuse_services
        if reuse_services and mode_choice == "both":
            raise ValueError(
                "--reuse-services requires --mode on or --mode off because "
                "VALIDATION_ENABLED is fixed when services start."
            )
        today = dt.date.today()
        self.prompts = [
            resolve_dynamic_prompt(prompt, today)
            for prompt in self.config["prompts"]
        ]
        if resume_dir is not None:
            self.session_dir = resume_dir.resolve()
            if not self.session_dir.exists():
                raise ValueError(
                    f"Resume directory does not exist: {self.session_dir}"
                )
        else:
            stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            self.session_dir = (
                self.output_root
                / f"{safe_name(self.config['experiment_name'])}-{stamp}"
            )
        self.summary_rows: list[dict[str, Any]] = []

    def load_completed_runs(self) -> set[tuple[str, str, int]]:
        """Load completed run.json files so a long experiment can resume."""
        completed: set[tuple[str, str, int]] = set()
        self.summary_rows = []
        for mode_name, _ in self.modes():
            mode_dir = self.session_dir / mode_name
            if not mode_dir.exists():
                continue
            for run_path in sorted(mode_dir.glob("*/run.json")):
                try:
                    row = json.loads(run_path.read_text(encoding="utf-8"))
                    key = (
                        str(row["mode"]),
                        str(row["prompt_id"]),
                        int(row["repetition"]),
                    )
                except (OSError, ValueError, KeyError, TypeError):
                    print(
                        f"Ignoring incomplete/corrupt run summary: {run_path}",
                        file=sys.stderr,
                    )
                    continue
                completed.add(key)
                self.summary_rows.append(row)
        return completed

    def modes(self) -> list[tuple[str, bool]]:
        if self.mode_choice == "on":
            return [("validation_on", True)]
        if self.mode_choice == "off":
            return [("validation_off", False)]
        return [("validation_on", True), ("validation_off", False)]

    def wait_for_completion(
        self,
        api: ApiClient,
        request_id: str,
        conversation: str,
    ) -> bool:
        timeout = float(self.config.get("run_timeout_seconds", 600))
        interval = float(self.config.get("poll_interval_seconds", 2))
        deadline = time.monotonic() + timeout
        seen_pending = False
        absent_count = 0
        consecutive_errors = 0
        error_limit = int(self.config.get("poll_error_limit", 8))
        started = time.monotonic()
        while time.monotonic() < deadline:
            try:
                pending_ids = {
                    str(item[0]) for item in api.pending() if item
                }
                consecutive_errors = 0
            except Exception as exc:
                consecutive_errors += 1
                print(
                    "Temporary polling error "
                    f"({consecutive_errors}/{error_limit}): {exc}"
                )
                if consecutive_errors >= error_limit:
                    raise RuntimeError(
                        "Host polling repeatedly failed; see Host-UI.log"
                    ) from exc
                time.sleep(interval)
                continue
            if request_id in pending_ids:
                seen_pending = True
                absent_count = 0
            else:
                try:
                    messages = api.list_messages(conversation)
                except Exception as exc:
                    consecutive_errors += 1
                    print(
                        "Temporary message-list error "
                        f"({consecutive_errors}/{error_limit}): {exc}"
                    )
                    if consecutive_errors >= error_limit:
                        raise RuntimeError(
                            "Host message queries repeatedly failed; "
                            "see Host-UI.log"
                        ) from exc
                    time.sleep(interval)
                    continue
                request_saved = any(message_id(item) == request_id for item in messages)
                if request_saved and (seen_pending or time.monotonic() - started >= 2):
                    absent_count += 1
                    if absent_count >= 2:
                        return True
            time.sleep(interval)
        return False

    @staticmethod
    def filter_new(
        items: list[dict[str, Any]], prior_ids: set[str], id_keys: tuple[str, ...]
    ) -> list[dict[str, Any]]:
        output = []
        for item in items:
            value = ""
            for key in id_keys:
                if item.get(key):
                    value = str(item[key])
                    break
            if not value or value not in prior_ids:
                output.append(item)
        return output

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
        calls = event_tool_calls(events)
        business_calls = [call for call in calls if call["name"] == "send_message"]
        model_called_order = [
            str(call["arguments"].get("agent_name"))
            for call in business_calls
            if call["arguments"].get("agent_name")
        ]
        model_call_messages = {
            str(call["arguments"].get("agent_name")): str(
                call["arguments"].get("message", "")
            )
            for call in business_calls
            if call["arguments"].get("agent_name")
        }
        model_used_agents = {
            str(call["arguments"].get("agent_name"))
            for call in business_calls
            if call["arguments"].get("agent_name")
        }
        wire_business_outgoing = [
            record
            for record in wire_trace
            if record.get("phase") == "business"
            and record.get("direction") == "outgoing"
        ]
        wire_called_order = [
            str(record.get("peer"))
            for record in wire_business_outgoing
            if record.get("peer")
        ]
        wire_call_messages = {
            str(record.get("peer")): trace_payload_text(record)
            for record in wire_business_outgoing
            if record.get("peer")
        }
        # Process-conformance metrics must use messages that actually crossed
        # the A2A boundary. Model tool-call events also contain calls rejected
        # by the validator and would otherwise make the enabled group look as
        # if those rejected calls had been sent.
        called_order = (
            wire_called_order if wire_trace else model_called_order
        )
        call_messages = (
            wire_call_messages if wire_trace else model_call_messages
        )
        wire_used_agents = {
            str(record.get("peer"))
            for record in wire_business_outgoing
            if record.get("peer")
        }
        # Once boundary tracing is available, an empty outgoing set means
        # that every model-side attempt was blocked before transmission.  Do
        # not count those attempts as actually covered remote agents.
        used_agents = sorted(
            wire_used_agents if wire_trace else model_used_agents
        )
        groups = self.config.get("expected_agent_groups", [])
        covered = sum(
            1 for group in groups if any(agent in used_agents for agent in group)
        )
        coverage_ratio = covered / len(groups) if groups else 1.0
        exclusive_violations = sum(
            1
            for group in self.config.get("exclusive_agent_groups", [])
            if sum(agent in used_agents for agent in group) > 1
        )
        exact_protocol_sequence = bool(groups) and (
            len(called_order) == len(groups)
            and all(
                called_order[index] in group
                for index, group in enumerate(groups)
            )
        )
        call_counts = Counter(called_order)
        repeated_agent_task = any(count > 1 for count in call_counts.values())
        redundant_calls = sum(max(count - 1, 0) for count in call_counts.values())
        actual_business_calls = len(called_order)
        nonrepeat_business_calls = actual_business_calls - redundant_calls
        communication_efficiency = (
            nonrepeat_business_calls / actual_business_calls
            if actual_business_calls
            else 0.0
        )
        blocked_model_calls = (
            max(len(business_calls) - len(wire_business_outgoing), 0)
            if wire_trace
            else 0
        )
        agent_messages = [
            item for item in messages if message_role(item).lower() == "agent"
        ]
        final_text = message_visible_text(agent_messages[-1]) if agent_messages else ""
        listed_failed_tasks = sum(
            task_state(task) == "failed" for task in tasks
        )
        wire_failed_task_ids = {
            str(
                (record.get("payload") or {}).get("id")
                or record.get("task_id")
                or f"wire-record-{index}"
            )
            for index, record in enumerate(wire_trace)
            if record.get("direction") == "incoming"
            and isinstance(record.get("payload"), dict)
            and task_state(record["payload"]) == "failed"
        }
        # The UI task/list endpoint can be empty even though an A2A response
        # contains a failed remote task. Count the most complete source.
        failed_tasks = max(
            listed_failed_tasks,
            len(wire_failed_task_ids),
        )
        log_error_markers = (
            log_text.count("[HOST VALIDATION ERROR]")
            + log_text.count("MPST tool-call violation")
            + log_text.count("MPST protocol violation")
        )
        final_response_is_error = bool(ERROR_FINAL_RE.search(final_text))
        task_completed = (
            bool(final_text)
            and not timed_out
            and failed_tasks == 0
            and not final_response_is_error
        )
        leak_detected = bool(TOOL_LEAK_RE.search(final_text))
        final_output_usable = (
            task_completed
            and not leak_detected
            and len(final_text.strip()) >= 200
        )
        prompt_text = next(
            (
                str(prompt.get("text", ""))
                for prompt in getattr(self, "prompts", [])
                if str(prompt.get("id")) == prompt_id
            ),
            "",
        )
        prompt_dates = re.findall(r"\d{4}-\d{2}-\d{2}", prompt_text)
        expected_dates = (
            (prompt_dates[0], prompt_dates[-1])
            if len(prompt_dates) >= 2
            else None
        )
        output_checklist = final_output_checklist(
            final_text,
            used_agents=set(used_agents),
            usable=final_output_usable,
            expected_dates=expected_dates,
        )
        output_completeness_score = sum(output_checklist.values())
        strict_full_execution = (
            task_completed
            and exact_protocol_sequence
            and failed_tasks == 0
            and not leak_detected
        )
        normalized_final = final_text.replace(" ", "")

        def before(first: str, second: str) -> bool:
            return (
                first in called_order
                and second in called_order
                and called_order.index(first) < called_order.index(second)
            )

        def contains_all(text: str, groups_to_match: list[list[str]]) -> bool:
            return all(any(word in text for word in group) for group in groups_to_match)

        weather_handoff = call_messages.get("Transport Select Agent", "")
        adverse_weather = any(
            word in weather_handoff
            for word in ("雨", "雪", "雷", "雾", "阴", "多云", "阵雨")
        )
        branch_matches_weather = (
            "Train Agent" in used_agents and "Flight Agent" not in used_agents
            if adverse_weather
            else exclusive_violations == 0
        )
        evidence = {
            "c1_weather_itinerary_evidence": (
                "Weather Agent" in used_agents
                and contains_all(
                    normalized_final,
                    [
                        ["天气", "晴", "雨", "雪", "阴"],
                        ["室内"],
                        ["户外"],
                    ],
                )
            ),
            "c2_weather_transport_evidence": (
                "Transport Select Agent" in used_agents
                and any(
                    word in weather_handoff
                    for word in ("天气", "晴", "雨", "雪", "阴", "多云")
                )
                and branch_matches_weather
            ),
            "c3_guide_ticket_evidence": before(
                "Guide Agent", "Ticket Agent"
            ),
            "c4_itinerary_budget_hotel_evidence": (
                before("Guide Agent", "Hotel Agent")
                and contains_all(
                    call_messages.get("Hotel Agent", ""),
                    [["预算", "10000", "一万"], ["行程", "攻略", "景点"]],
                )
            ),
            "c5_daily_route_evidence": (
                "Public Transport Agent" in used_agents
                and contains_all(
                    normalized_final,
                    [
                        ["地铁", "公交", "交通工具"],
                        ["换乘", "路线"],
                        ["元", "价格", "费用"],
                    ],
                )
            ),
            "c6_expense_per_capita_evidence": (
                "Budget Agent" in used_agents
                and contains_all(
                    normalized_final,
                    [["人均", "每人"], ["总费用", "总计", "合计"], ["预算"]],
                )
            ),
        }
        evidence_total = sum(bool(value) for value in evidence.values())
        process_score = round(
            (2 if task_completed else 0)
            + 3 * coverage_ratio
            + (3 if exact_protocol_sequence else 0)
            + (1 if failed_tasks == 0 else 0)
            + (1 if not leak_detected else 0),
            2,
        )
        return {
            "run_id": run_id,
            "mode": mode_name,
            "prompt_id": prompt_id,
            "repetition": repetition,
            "conversation_id": conversation,
            "duration_seconds": round(duration, 3),
            "timed_out": timed_out,
            "task_completed": task_completed,
            "strict_full_execution": strict_full_execution,
            "final_output_usable": final_output_usable,
            "final_response_visible": bool(final_text),
            "final_response_is_error": final_response_is_error,
            "final_response_chars": len(final_text),
            "business_send_message_calls": (
                len(wire_business_outgoing)
                if wire_trace
                else len(business_calls)
            ),
            "model_send_message_tool_calls": len(business_calls),
            "blocked_send_message_calls": blocked_model_calls,
            "a2a_trace_records": len(wire_trace),
            "all_host_tool_calls": len(calls),
            "used_agent_count": len(used_agents),
            "used_agents": "|".join(used_agents),
            "required_stage_coverage_count": covered,
            "required_group_coverage": f"{covered}/{len(groups)}",
            "required_group_coverage_ratio": round(coverage_ratio, 4),
            "exclusive_branch_violations": exclusive_violations,
            "exact_protocol_sequence": exact_protocol_sequence,
            "repeated_agent_task": repeated_agent_task,
            "redundant_business_calls": redundant_calls,
            "nonrepeat_business_calls": nonrepeat_business_calls,
            "communication_efficiency": round(communication_efficiency, 4),
            "failed_remote_tasks": failed_tasks,
            "tool_call_leak_in_final": leak_detected,
            "finalize_protocol_calls": sum(
                call["name"] == "finalize_protocol" for call in calls
            ),
            "validation_log_markers": log_error_markers,
            **output_checklist,
            "output_completeness_score_0_6": output_completeness_score,
            **evidence,
            "automatic_task_point_evidence_0_6": evidence_total,
            "process_score_0_10": process_score,
            "message_count": len(messages),
            "event_count": len(events),
            "task_count": len(tasks),
        }

    def run_one(
        self,
        api: ApiClient,
        group: ServiceGroup | None,
        mode_dir: Path,
        mode_name: str,
        prompt: dict[str, str],
        repetition: int,
    ) -> None:
        run_id = f"{mode_name}-{safe_name(prompt['id'])}-r{repetition:02d}"
        run_dir = mode_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        before_events = api.list_events()
        before_tasks = api.list_tasks()
        prior_event_ids = {str(item.get("id")) for item in before_events}
        prior_task_ids = {str(item.get("id")) for item in before_tasks}
        offsets = group.log_offsets() if group else {}
        conversation_data = api.create_conversation()
        conversation = str(
            conversation_data.get("conversation_id")
            or conversation_data.get("conversationId")
            or ""
        )
        if not conversation:
            raise RuntimeError("Host returned an empty conversation id")

        started = time.monotonic()
        request_id = api.send_message(conversation, prompt["text"])
        completed = self.wait_for_completion(api, request_id, conversation)
        duration = time.monotonic() - started
        time.sleep(float(self.config.get("settle_seconds", 1)))
        messages = api.list_messages(conversation)
        events = self.filter_new(
            api.list_events(), prior_event_ids, ("id",)
        )
        tasks = self.filter_new(
            api.list_tasks(), prior_task_ids, ("id", "task_id", "taskId")
        )
        if group:
            log_text = group.copy_log_slices(offsets, run_dir / "process_logs")
        else:
            log_text = ""
        wire_trace = parse_a2a_trace(log_text)

        rows = communication_rows(run_id, messages, events)
        fields = [
            "run_id", "sequence", "source", "timestamp", "actor", "role",
            "message_id", "context_id", "task_id", "part_index", "part_kind",
            "content",
        ]
        csv_dump(run_dir / "communications.csv", rows, fields)
        json_dump(run_dir / "messages.json", messages)
        json_dump(run_dir / "events.json", events)
        json_dump(run_dir / "tasks.json", tasks)
        json_dump(run_dir / "tool_calls.json", event_tool_calls(events))
        json_dump(run_dir / "a2a_trace.json", wire_trace)
        trace_rows = [
            {
                "run_id": run_id,
                "timestamp": record.get("timestamp", ""),
                "direction": record.get("direction", ""),
                "phase": record.get("phase", ""),
                "peer": record.get("peer", ""),
                "context_id": record.get("context_id", ""),
                "task_id": record.get("task_id", ""),
                "message_id": record.get("message_id", ""),
                "payload": json.dumps(
                    record.get("payload"), ensure_ascii=False, default=str
                ),
            }
            for record in wire_trace
        ]
        csv_dump(
            run_dir / "a2a_trace.csv",
            trace_rows,
            [
                "run_id", "timestamp", "direction", "phase", "peer",
                "context_id", "task_id", "message_id", "payload",
            ],
        )
        (run_dir / "prompt.txt").write_text(prompt["text"], encoding="utf-8")
        summary = self.analyze(
            run_id,
            mode_name,
            prompt["id"],
            repetition,
            conversation,
            duration,
            not completed,
            messages,
            events,
            tasks,
            log_text,
            wire_trace,
        )
        json_dump(run_dir / "run.json", summary)
        final_messages = [
            item for item in messages if message_role(item).lower() == "agent"
        ]
        final_text = (
            message_visible_text(final_messages[-1]) if final_messages else ""
        )
        (run_dir / "final_response.txt").write_text(
            final_text, encoding="utf-8"
        )
        self.summary_rows.append(summary)
        print(
            self.format_terminal_summary(
                mode_name, prompt, repetition, summary
            )
        )

    def format_terminal_summary(
        self,
        mode_name: str,
        prompt: dict[str, str],
        repetition: int,
        summary: dict[str, Any],
    ) -> str:
        """Format the one-line terminal summary for a completed run."""
        return (
            f"[{mode_name}] {prompt['id']} repetition {repetition}: "
            f"completed={summary['task_completed']} "
            f"agents={summary['used_agent_count']} "
            f"calls={summary['business_send_message_calls']} "
            f"score={summary['process_score_0_10']}"
        )

    def register_agents(self, api: ApiClient) -> None:
        remotes = [
            service
            for service in self.config["services"]
            if service.get("role") == "remote"
        ]
        for service in remotes:
            api.register_agent(str(service["url"]))
        expected = {str(service["name"]) for service in remotes}
        actual = {str(agent.get("name")) for agent in api.list_agents()}
        if len(actual) < len(expected):
            raise RuntimeError(
                f"Only {len(actual)}/{len(expected)} remote agents registered: "
                f"{sorted(actual)}"
            )

    def write_tables(self) -> None:
        if not self.summary_rows:
            return
        summary_fields = list(self.summary_rows[0].keys())
        csv_dump(
            self.session_dir / "summary.csv",
            self.summary_rows,
            summary_fields,
        )

        aggregate_rows = []
        numeric_fields = [
            "task_completed",
            "strict_full_execution",
            "final_output_usable",
            "final_response_is_error",
            "duration_seconds",
            "business_send_message_calls",
            "model_send_message_tool_calls",
            "blocked_send_message_calls",
            "used_agent_count",
            "required_stage_coverage_count",
            "required_group_coverage_ratio",
            "exclusive_branch_violations",
            "exact_protocol_sequence",
            "repeated_agent_task",
            "redundant_business_calls",
            "nonrepeat_business_calls",
            "communication_efficiency",
            "failed_remote_tasks",
            "tool_call_leak_in_final",
            "validation_log_markers",
            "output_completeness_score_0_6",
            "process_score_0_10",
        ]
        for mode, _ in self.modes():
            selected = [row for row in self.summary_rows if row["mode"] == mode]
            if not selected:
                continue
            aggregate = {"mode": mode, "runs": len(selected)}
            for field in numeric_fields:
                total = sum(float(row[field]) for row in selected)
                aggregate[f"total_{field}"] = round(total, 4)
                aggregate[f"mean_{field}"] = round(total / len(selected), 4)
            aggregate_rows.append(aggregate)
        if aggregate_rows:
            csv_dump(
                self.session_dir / "aggregate.csv",
                aggregate_rows,
                list(aggregate_rows[0].keys()),
            )

        paired_rows = []
        indexes = {
            (row["mode"], row["prompt_id"], row["repetition"]): row
            for row in self.summary_rows
        }
        for prompt in self.prompts:
            for repetition in range(1, self.repetitions + 1):
                on = indexes.get(("validation_on", prompt["id"], repetition))
                off = indexes.get(("validation_off", prompt["id"], repetition))
                if not on or not off:
                    continue
                pair = {
                    "prompt_id": prompt["id"],
                    "repetition": repetition,
                }
                for field in (
                    "task_completed",
                    "strict_full_execution",
                    "final_output_usable",
                    "business_send_message_calls",
                    "blocked_send_message_calls",
                    "used_agent_count",
                    "required_stage_coverage_count",
                    "exclusive_branch_violations",
                    "exact_protocol_sequence",
                    "repeated_agent_task",
                    "redundant_business_calls",
                    "communication_efficiency",
                    "output_completeness_score_0_6",
                    "tool_call_leak_in_final",
                    "process_score_0_10",
                    "duration_seconds",
                ):
                    pair[f"on_{field}"] = on[field]
                    pair[f"off_{field}"] = off[field]
                    pair[f"delta_on_minus_off_{field}"] = round(
                        float(on[field]) - float(off[field]), 4
                    )
                paired_rows.append(pair)
        if paired_rows:
            csv_dump(
                self.session_dir / "paired_comparison.csv",
                paired_rows,
                list(paired_rows[0].keys()),
            )

    def dry_run(self) -> Path:
        self.session_dir.mkdir(parents=True, exist_ok=True)
        json_dump(
            self.session_dir / "resolved_prompts.json",
            self.prompts,
        )
        json_dump(
            self.session_dir / "reproducibility.json",
            reproducibility_metadata(self.project_root),
        )
        print(f"Resolved prompts written to {self.session_dir}")
        return self.session_dir

    def run(self) -> Path:
        self.session_dir.mkdir(parents=True, exist_ok=True)
        completed_runs = self.load_completed_runs()
        snapshot = dict(self.config)
        snapshot["prompts"] = self.prompts
        snapshot["repetitions"] = self.repetitions
        if completed_runs:
            snapshot["resumed_at"] = utc_now()
            snapshot["preexisting_run_count"] = len(completed_runs)
        else:
            snapshot["started_at"] = utc_now()
        snapshot["mode_choice"] = self.mode_choice
        snapshot["reproducibility"] = reproducibility_metadata(
            self.project_root
        )
        json_dump(self.session_dir / "config.snapshot.json", snapshot)

        api = ApiClient(
            str(self.config.get("host_base_url", "http://127.0.0.1:12000")),
            timeout=float(self.config.get("http_timeout_seconds", 30)),
        )
        for mode_name, enabled in self.modes():
            mode_dir = self.session_dir / mode_name
            mode_dir.mkdir(parents=True, exist_ok=True)
            pending_runs = [
                (prompt, repetition)
                for prompt in self.prompts
                for repetition in range(1, self.repetitions + 1)
                if (mode_name, prompt["id"], repetition) not in completed_runs
            ]
            if not pending_runs:
                print(f"Skipping {mode_name}: all runs already completed.")
                continue
            group: ServiceGroup | None = None
            try:
                if not self.reuse_services:
                    explicit_env = {
                        str(key): str(value)
                        for key, value in self.config.get("environment", {}).items()
                    }
                    explicit_env["VALIDATION_ENABLED"] = (
                        "true" if enabled else "false"
                    )
                    group = ServiceGroup(
                        self.project_root,
                        self.config["services"],
                        mode_dir,
                        explicit_env,
                    )
                    print(f"Starting services for {mode_name}...")
                    group.start(
                        float(self.config.get("startup_timeout_seconds", 180))
                    )
                else:
                    print(f"Reusing already running services for {mode_name}...")
                    api.list_agents()
                self.register_agents(api)
                for prompt, repetition in pending_runs:
                    self.run_one(
                        api,
                        group,
                        mode_dir,
                        mode_name,
                        prompt,
                        repetition,
                    )
            finally:
                if group:
                    print(f"Stopping services for {mode_name}...")
                    group.stop()
        self.write_tables()
        manifest = {
            "experiment_name": self.config["experiment_name"],
            "completed_at": utc_now(),
            "run_count": len(self.summary_rows),
            "result_directory": str(self.session_dir),
        }
        json_dump(self.session_dir / "manifest.json", manifest)
        return self.session_dir


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automate paired MPST-A2A experiments."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/travel_experiment.json"),
        help="Experiment JSON configuration.",
    )
    parser.add_argument(
        "--mode",
        choices=("both", "on", "off"),
        default="both",
        help="Run both groups or one validation mode.",
    )
    parser.add_argument(
        "--repetitions",
        type=int,
        help="Override repetitions from the configuration.",
    )
    parser.add_argument(
        "--reuse-services",
        action="store_true",
        help="Use services already running; only valid with --mode on/off.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        help="Override the result root directory.",
    )
    parser.add_argument(
        "--resume-dir",
        type=Path,
        help=(
            "Resume an interrupted experiment in an existing result directory; "
            "completed run.json files are skipped."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only resolve and save the paired prompts.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.repetitions is not None and args.repetitions < 1:
        raise ValueError("--repetitions must be at least 1")
    runner = ExperimentRunner(
        args.config,
        mode_choice=args.mode,
        repetitions=args.repetitions,
        reuse_services=args.reuse_services,
        output_root=args.output_root,
        resume_dir=args.resume_dir,
    )
    result = runner.dry_run() if args.dry_run else runner.run()
    print(f"Experiment results: {result}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Experiment interrupted by user.", file=sys.stderr)
        raise SystemExit(130)
