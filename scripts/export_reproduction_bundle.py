"""Export a compact, non-secret paper-result bundle from a full run."""

from __future__ import annotations

import argparse
import json
import shutil

from pathlib import Path

try:
    from .experiment_runner import (
        json_dump,
        message_role,
        message_visible_text,
    )
except ImportError:
    from experiment_runner import (  # type: ignore[no-redef]
        json_dump,
        message_role,
        message_visible_text,
    )


METADATA_FILES = (
    "summary.csv",
    "aggregate.csv",
    "paired_comparison.csv",
    "config.snapshot.json",
    "resolved_prompts.json",
    "manifest.json",
)


def final_agent_message(messages: list[dict]) -> dict | None:
    selected = [
        message for message in messages if message_role(message).lower() == "agent"
    ]
    return selected[-1] if selected else None


def export_bundle(source: Path, destination: Path) -> Path:
    source = source.resolve()
    destination = destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValueError(f"Destination is not empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)

    for name in METADATA_FILES:
        source_path = source / name
        if source_path.exists():
            shutil.copy2(source_path, destination / name)

    final_outputs = []
    for run_path in sorted(source.glob("validation_*/*/run.json")):
        run_dir = run_path.parent
        relative_dir = run_dir.relative_to(source)
        target_dir = destination / relative_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(run_path, target_dir / "run.json")

        messages_path = run_dir / "messages.json"
        messages = (
            json.loads(messages_path.read_text(encoding="utf-8"))
            if messages_path.exists()
            else []
        )
        final_message = final_agent_message(messages)
        minimal_messages = [final_message] if final_message else []
        json_dump(target_dir / "messages.json", minimal_messages)

        run = json.loads(run_path.read_text(encoding="utf-8"))
        final_outputs.append(
            {
                "run_id": run.get("run_id", run_dir.name),
                "mode": run.get("mode", relative_dir.parts[0]),
                "prompt_id": run.get("prompt_id", ""),
                "repetition": run.get("repetition", ""),
                "final_output": (
                    message_visible_text(final_message) if final_message else ""
                ),
            }
        )

    jsonl_path = destination / "final_outputs.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as stream:
        for row in final_outputs:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export final outputs and summary data for paper reproduction."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    output = export_bundle(args.source, args.destination)
    print(f"Reproduction bundle: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
