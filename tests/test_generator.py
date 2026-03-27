"""Tests for benchmark task generation."""

from subprocess import run

from harness_eval.generator.git_analyzer import (
    FIX_PATTERN,
    TEST_PATH_PATTERN,
    estimate_difficulty,
    get_fix_commits,
)
from harness_eval.generator.models import BenchmarkTask
from harness_eval.generator.pipeline import generate_tasks


def _init_git_repo(tmp_path):
    """Create a git repo with a fix commit that has test changes."""
    run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    run(
        ["git", "-C", str(tmp_path), "config", "user.email", "test@test.com"],
        check=True,
        capture_output=True,
    )
    run(
        ["git", "-C", str(tmp_path), "config", "user.name", "Test"],
        check=True,
        capture_output=True,
    )

    # Initial commit with source + test
    src = tmp_path / "src"
    src.mkdir()
    (src / "app.py").write_text("def greet():\n    return 'hello'\n")
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_app.py").write_text(
        "from src.app import greet\n\n"
        "def test_greet():\n"
        "    assert greet() == 'hello'\n"
    )
    run(
        ["git", "-C", str(tmp_path), "add", "."],
        check=True,
        capture_output=True,
    )
    run(
        ["git", "-C", str(tmp_path), "commit", "-m", "initial commit"],
        check=True,
        capture_output=True,
    )

    # Fix commit: change source + add test
    (src / "app.py").write_text(
        "def greet(name='world'):\n    return f'hello {name}'\n"
    )
    (tests / "test_app.py").write_text(
        "from src.app import greet\n\n"
        "def test_greet():\n"
        "    assert greet() == 'hello world'\n\n"
        "def test_greet_name():\n"
        "    assert greet('alice') == 'hello alice'\n"
    )
    run(
        ["git", "-C", str(tmp_path), "add", "."],
        check=True,
        capture_output=True,
    )
    run(
        ["git", "-C", str(tmp_path), "commit", "-m", "fix: greet default name bug"],
        check=True,
        capture_output=True,
    )
    return tmp_path


def test_fix_pattern_matches():
    assert FIX_PATTERN.search("fix: broken login")
    assert FIX_PATTERN.search("Bug in parser resolved")
    assert FIX_PATTERN.search("closes #123")
    assert not FIX_PATTERN.search("feat: add new feature")


def test_test_path_pattern():
    assert TEST_PATH_PATTERN.search("tests/test_app.py")
    assert TEST_PATH_PATTERN.search("spec/auth_spec.rb")
    assert TEST_PATH_PATTERN.search("src/app_test.go")
    assert not TEST_PATH_PATTERN.search("src/app.py")


def test_get_fix_commits(tmp_path):
    repo = _init_git_repo(tmp_path)
    commits = get_fix_commits(repo)
    assert len(commits) == 1
    assert "fix" in commits[0].message.lower()
    assert len(commits[0].test_files) > 0
    assert len(commits[0].source_files) > 0


def test_generate_tasks(tmp_path):
    repo = _init_git_repo(tmp_path)
    tasks = generate_tasks(repo)
    assert len(tasks) == 1
    task = tasks[0]
    assert isinstance(task, BenchmarkTask)
    assert "fix" in task.description.lower()
    assert task.test_patch
    assert task.files_changed


def test_estimate_difficulty():
    from harness_eval.generator.git_analyzer import FixCommit

    easy = FixCommit(sha="a", message="fix", source_files=["a.py"])
    assert estimate_difficulty(easy) == "easy"

    medium = FixCommit(sha="a", message="fix", source_files=["a.py", "b.py"])
    assert estimate_difficulty(medium) == "medium"

    hard = FixCommit(sha="a", message="fix", source_files=["a", "b", "c", "d"])
    assert estimate_difficulty(hard) == "hard"


def test_benchmark_task_to_dict():
    task = BenchmarkTask(
        id="test-001",
        description="Fix bug",
        repo="https://github.com/u/r",
        base_commit="abc",
        fix_commit="def",
        test_patch="diff...",
    )
    d = task.to_dict()
    assert d["id"] == "test-001"
    assert d["repo"] == "https://github.com/u/r"
    assert isinstance(d["files_changed"], list)
