"""Analyze git history to find bug-fix commits with test changes."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from subprocess import CalledProcessError, run

FIX_PATTERN = re.compile(
    r"\b(fix|bug|close|closes|closed|resolve|resolves|resolved|patch|hotfix)\b",
    re.IGNORECASE,
)

TEST_PATH_PATTERN = re.compile(
    r"(test[s_/]|spec[s_/]|_test\.|\.test\.|\.spec\.)",
    re.IGNORECASE,
)


@dataclass
class FixCommit:
    """A commit that looks like a bug fix with test changes."""

    sha: str
    message: str
    files_changed: list[str] = field(default_factory=list)
    test_files: list[str] = field(default_factory=list)
    source_files: list[str] = field(default_factory=list)
    parent_sha: str = ""


def _run_git(project: Path, *args: str) -> str:
    try:
        result = run(
            ["git", "-C", str(project), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except CalledProcessError:
        return ""


def get_fix_commits(
    project: Path,
    max_commits: int = 500,
    include_merges: bool = False,
) -> list[FixCommit]:
    """Scan git log for bug-fix commits that include test changes."""
    fmt = "%H%x00%P%x00%s"
    args = ["log", f"--format={fmt}", f"-n{max_commits}"]
    if not include_merges:
        args.append("--no-merges")

    log_output = _run_git(project, *args)
    if not log_output:
        return []

    commits: list[FixCommit] = []
    for line in log_output.splitlines():
        parts = line.split("\x00")
        if len(parts) < 3:
            continue
        sha, parents, message = parts[0], parts[1], parts[2]
        if not FIX_PATTERN.search(message):
            continue

        parent = parents.split()[0] if parents else ""
        if not parent:
            continue

        files_raw = _run_git(project, "diff", "--name-only", parent, sha)
        if not files_raw:
            continue
        files = files_raw.splitlines()
        test_files = [f for f in files if TEST_PATH_PATTERN.search(f)]
        source_files = [f for f in files if not TEST_PATH_PATTERN.search(f)]

        if not test_files or not source_files:
            continue

        commits.append(
            FixCommit(
                sha=sha,
                message=message,
                files_changed=files,
                test_files=test_files,
                source_files=source_files,
                parent_sha=parent,
            )
        )

    return commits


def get_test_patch(project: Path, parent: str, sha: str, test_files: list[str]) -> str:
    """Extract the test-only diff between parent and fix commit."""
    if not test_files:
        return ""
    return _run_git(project, "diff", parent, sha, "--", *test_files)


def estimate_difficulty(commit: FixCommit) -> str:
    """Heuristic difficulty based on files changed."""
    n = len(commit.source_files)
    if n <= 1:
        return "easy"
    if n <= 3:
        return "medium"
    return "hard"
