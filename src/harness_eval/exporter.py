"""Export benchmark tasks to SWE-bench compatible format."""

import json
from pathlib import Path

import yaml


def to_swebench(tasks_dir: Path) -> list[dict]:
    """Convert harness-eval tasks to SWE-bench JSONL format."""
    entries = []
    for tf in sorted(tasks_dir.glob("*.yaml")):
        data = yaml.safe_load(tf.read_text())
        entry = {
            "instance_id": data["id"],
            "repo": data.get("repo", ""),
            "base_commit": data["base_commit"],
            "problem_statement": data["description"],
            "hints_text": "\n".join(data.get("hints", [])),
            "test_patch": data["test_patch"],
            "FAIL_TO_PASS": [],
            "PASS_TO_PASS": [],
            "environment_setup_commit": data["base_commit"],
        }
        entries.append(entry)
    return entries


def to_jsonl(tasks_dir: Path, output: Path) -> int:
    """Write SWE-bench compatible JSONL file. Returns task count."""
    entries = to_swebench(tasks_dir)
    with output.open("w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    return len(entries)


def to_csv(tasks_dir: Path, output: Path) -> int:
    """Write CSV summary of benchmark tasks. Returns task count."""
    import csv

    task_files = sorted(tasks_dir.glob("*.yaml"))
    if not task_files:
        return 0

    with output.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "id",
                "description",
                "difficulty",
                "files_changed",
                "base_commit",
            ]
        )
        for tf in task_files:
            data = yaml.safe_load(tf.read_text())
            writer.writerow(
                [
                    data["id"],
                    data["description"],
                    data.get("difficulty", "medium"),
                    "|".join(data.get("files_changed", [])),
                    data["base_commit"],
                ]
            )
    return len(task_files)
