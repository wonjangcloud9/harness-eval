"""Tests for benchmark runner."""

from harness_eval.runner import TaskResult


def test_task_result_pass():
    r = TaskResult(task_id="t1", passed=True)
    assert r.passed
    assert r.error == ""


def test_task_result_fail():
    r = TaskResult(task_id="t2", passed=False, error="patch failed")
    assert not r.passed
    assert "patch" in r.error
