"""Watch project for changes and re-score automatically."""

import time
from pathlib import Path

from harness_eval.scanner import scan

WATCH_PATTERNS = [
    "CLAUDE.md",
    "AGENTS.md",
    ".cursorrules",
    "ARCHITECTURE.md",
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    ".gitignore",
    ".pre-commit-config.yaml",
    "Dockerfile",
    "docker-compose.yml",
    "pyproject.toml",
    "package.json",
    "go.mod",
    "Cargo.toml",
    ".github",
    "docs",
]


def _get_mtimes(project: Path) -> dict[str, float]:
    mtimes: dict[str, float] = {}
    for pattern in WATCH_PATTERNS:
        target = project / pattern
        if target.exists():
            if target.is_dir():
                for f in target.rglob("*"):
                    if f.is_file():
                        mtimes[str(f)] = f.stat().st_mtime
            else:
                mtimes[str(target)] = target.stat().st_mtime
    return mtimes


def watch_and_score(
    project: Path,
    interval: float = 2.0,
    callback=None,
):
    """Watch for file changes and re-score.

    Args:
        project: Project directory to watch.
        interval: Seconds between checks.
        callback: Called with (Scorecard, changed_files) on each change.
                  If None, prints to console.
    """
    last_mtimes = _get_mtimes(project)
    card = scan(project)

    if callback:
        callback(card, [])
    else:
        _default_print(card, [])

    while True:
        time.sleep(interval)
        current_mtimes = _get_mtimes(project)

        changed = []
        for path, mtime in current_mtimes.items():
            if path not in last_mtimes or last_mtimes[path] != mtime:
                changed.append(path)
        for path in last_mtimes:
            if path not in current_mtimes:
                changed.append(path)

        if changed:
            card = scan(project)
            if callback:
                callback(card, changed)
            else:
                _default_print(card, changed)
            last_mtimes = current_mtimes


def _default_print(card, changed: list[str]):
    from rich.console import Console

    c = Console()
    if changed:
        short = [Path(f).name for f in changed[:3]]
        extra = f" (+{len(changed)-3} more)" if len(changed) > 3 else ""
        c.print(f"\n[dim]Changed: {', '.join(short)}{extra}[/dim]")
    c.print(
        f"  Grade: [{_grade_color(card.grade)}]{card.grade}[/]"
        f"  Score: {card.percentage:.0f}%"
    )


def _grade_color(grade: str) -> str:
    return {
        "A": "green",
        "B": "blue",
        "C": "yellow",
        "D": "red",
        "F": "bright_red",
    }.get(grade, "white")
