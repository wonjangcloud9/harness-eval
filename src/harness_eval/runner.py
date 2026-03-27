"""Run benchmark tasks against a repo to verify fixes."""

import tempfile
from dataclasses import dataclass
from pathlib import Path
from subprocess import CalledProcessError, run


@dataclass
class TaskResult:
    """Result of running a single benchmark task."""

    task_id: str
    passed: bool
    error: str = ""


def _run_cmd(cwd: str, *args: str) -> tuple[bool, str]:
    try:
        result = run(
            list(args),
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return True, result.stdout
    except CalledProcessError as exc:
        return False, exc.stderr
    except TimeoutError:
        return False, "Command timed out (120s)"


def run_task(
    repo_path: Path,
    base_commit: str,
    test_patch: str,
    task_id: str = "",
) -> TaskResult:
    """Run a single benchmark task.

    1. Create a temp worktree at base_commit
    2. Apply the test patch
    3. Run the test suite to verify it fails (test catches the bug)
    4. Clean up
    """
    with tempfile.TemporaryDirectory(prefix="harness-run-") as tmpdir:
        # Create worktree at base commit
        ok, err = _run_cmd(
            str(repo_path),
            "git",
            "worktree",
            "add",
            "--detach",
            tmpdir,
            base_commit,
        )
        if not ok:
            return TaskResult(
                task_id=task_id, passed=False, error=f"Worktree failed: {err}"
            )

        try:
            # Apply test patch
            patch_file = Path(tmpdir) / ".harness-test.patch"
            patch_file.write_text(test_patch)
            ok, err = _run_cmd(tmpdir, "git", "apply", "--allow-empty", str(patch_file))
            if not ok:
                return TaskResult(
                    task_id=task_id, passed=False, error=f"Patch failed: {err}"
                )

            # The test should FAIL on the base commit (bug exists)
            ok, _ = _run_cmd(tmpdir, "python", "-m", "pytest", "--tb=short", "-q")

            # If tests fail, the benchmark is valid (test catches the bug)
            return TaskResult(task_id=task_id, passed=not ok)
        finally:
            _run_cmd(str(repo_path), "git", "worktree", "remove", "--force", tmpdir)


def run_benchmark(
    repo_path: Path,
    tasks_dir: Path,
) -> list[TaskResult]:
    """Run all benchmark tasks in a directory."""
    import yaml

    results: list[TaskResult] = []
    task_files = sorted(tasks_dir.glob("*.yaml"))

    for tf in task_files:
        data = yaml.safe_load(tf.read_text())
        result = run_task(
            repo_path=repo_path,
            base_commit=data["base_commit"],
            test_patch=data["test_patch"],
            task_id=data.get("id", tf.stem),
        )
        results.append(result)

    return results
