"""Pipeline: combine git analysis into benchmark tasks."""

import re
from pathlib import Path

from harness_eval.config import HarnessConfig, load_config
from harness_eval.generator.git_analyzer import (
    estimate_difficulty,
    get_fix_commits,
    get_test_patch,
)
from harness_eval.generator.models import BenchmarkTask


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60]


def _get_repo_url(project: Path) -> str:
    """Try to extract remote origin URL."""
    from subprocess import CalledProcessError, run

    try:
        result = run(
            ["git", "-C", str(project), "remote", "get-url", "origin"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (CalledProcessError, FileNotFoundError):
        return str(project)


def _build_hints(source_files: list[str]) -> list[str]:
    hints = []
    if len(source_files) == 1:
        hints.append(f"The fix is in {source_files[0]}")
    else:
        dirs = {str(Path(f).parent) for f in source_files}
        if len(dirs) == 1:
            hints.append(f"Look in the {dirs.pop()}/ directory")
        else:
            hints.append(
                f"Changes span {len(source_files)} files"
                f" across {len(dirs)} directories"
            )
    return hints


def generate_tasks(
    project: Path,
    config: HarnessConfig | None = None,
) -> list[BenchmarkTask]:
    """Generate benchmark tasks from a project's git history."""
    if config is None:
        config = load_config(project)

    gen_cfg = config.generate
    commits = get_fix_commits(
        project,
        max_commits=gen_cfg.max_tasks * 10,
        include_merges=gen_cfg.include_merge_commits,
    )

    repo_url = _get_repo_url(project)
    tasks: list[BenchmarkTask] = []

    for i, commit in enumerate(commits):
        if len(tasks) >= gen_cfg.max_tasks:
            break

        test_patch = get_test_patch(
            project, commit.parent_sha, commit.sha, commit.test_files
        )
        if not test_patch:
            continue

        test_lines = sum(
            1
            for line in test_patch.splitlines()
            if line.startswith("+") and not line.startswith("+++")
        )
        if test_lines < gen_cfg.min_test_lines:
            continue

        task_id = f"{_slugify(commit.message)}-{commit.sha[:7]}"
        tasks.append(
            BenchmarkTask(
                id=task_id,
                description=commit.message,
                repo=repo_url,
                base_commit=commit.parent_sha,
                fix_commit=commit.sha,
                test_patch=test_patch,
                files_changed=commit.source_files,
                hints=_build_hints(commit.source_files),
                difficulty=estimate_difficulty(commit),
            )
        )

    return tasks
