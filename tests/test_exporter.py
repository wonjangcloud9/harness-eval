"""Tests for benchmark export functionality."""

import json

import yaml

from harness_eval.exporter import to_csv, to_jsonl, to_swebench


def _create_task_file(tasks_dir, task_id="fix-bug-abc1234"):
    tasks_dir.mkdir(exist_ok=True)
    task = {
        "id": task_id,
        "description": "Fix login bug",
        "repo": "https://github.com/u/r",
        "base_commit": "abc123",
        "fix_commit": "def456",
        "test_patch": "diff --git a/t.py b/t.py\n+assert True",
        "files_changed": ["src/auth.py"],
        "hints": ["Check auth module"],
        "difficulty": "easy",
    }
    (tasks_dir / f"{task_id}.yaml").write_text(yaml.dump(task))
    return tasks_dir


def test_to_swebench(tmp_path):
    tasks_dir = _create_task_file(tmp_path / "bench")
    entries = to_swebench(tasks_dir)
    assert len(entries) == 1
    e = entries[0]
    assert e["instance_id"] == "fix-bug-abc1234"
    assert e["base_commit"] == "abc123"
    assert "test_patch" in e
    assert "hints_text" in e


def test_to_jsonl(tmp_path):
    tasks_dir = _create_task_file(tmp_path / "bench")
    out = tmp_path / "output.jsonl"
    count = to_jsonl(tasks_dir, out)
    assert count == 1
    lines = out.read_text().strip().splitlines()
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["instance_id"] == "fix-bug-abc1234"


def test_to_csv(tmp_path):
    tasks_dir = _create_task_file(tmp_path / "bench")
    out = tmp_path / "output.csv"
    count = to_csv(tasks_dir, out)
    assert count == 1
    content = out.read_text()
    assert "fix-bug-abc1234" in content
    assert "easy" in content


def test_empty_tasks_dir(tmp_path):
    tasks_dir = tmp_path / "empty"
    tasks_dir.mkdir()
    entries = to_swebench(tasks_dir)
    assert entries == []
    count = to_csv(tasks_dir, tmp_path / "out.csv")
    assert count == 0
