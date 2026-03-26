"""Tests for the harness-eval scanner."""

from pathlib import Path

from harness_eval.models import Scorecard
from harness_eval.scanner import scan


def test_scan_returns_scorecard(tmp_path: Path):
    card = scan(tmp_path)
    assert isinstance(card, Scorecard)
    assert len(card.dimensions) == 7


def test_empty_project_low_score(tmp_path: Path):
    card = scan(tmp_path)
    assert card.percentage < 15.0  # entropy passes vacuously


def test_context_file_boosts_score(tmp_path: Path):
    (tmp_path / "CLAUDE.md").write_text("# Rules")
    card = scan(tmp_path)
    ctx = next(
        d for d in card.dimensions
        if d.name == "Context Engineering"
    )
    assert ctx.score > 0.0


def test_full_project_scores_higher(tmp_path: Path):
    (tmp_path / "CLAUDE.md").write_text("# ctx")
    (tmp_path / "README.md").write_text("# hi")
    (tmp_path / ".gitignore").write_text("*.pyc")
    (tmp_path / "Dockerfile").write_text("FROM python")
    (tmp_path / "poetry.lock").write_text("")
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "workflows").mkdir()
    (tmp_path / "pyproject.toml").write_text("[tool]")

    card = scan(tmp_path)
    assert card.percentage > 50.0
