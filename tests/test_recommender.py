"""Tests for recommendation engine."""

from pathlib import Path

from harness_eval.recommender import get_recommendations
from harness_eval.scanner import scan


def test_empty_project_gets_all_recs(tmp_path: Path):
    card = scan(tmp_path)
    recs = get_recommendations(card)
    assert len(recs) == 7
    assert recs[0]["current_pct"] == 0.0


def test_full_project_fewer_recs(tmp_path: Path):
    (tmp_path / "CLAUDE.md").write_text("## Rules\n- rule1")
    (tmp_path / "AGENTS.md").write_text("## Agent config")
    (tmp_path / "README.md").write_text("# Project")
    (tmp_path / "CONTRIBUTING.md").write_text("# How")
    (tmp_path / "CHANGELOG.md").write_text("# v1")
    (tmp_path / ".gitignore").write_text("*.pyc")
    (tmp_path / "Dockerfile").write_text("FROM python")
    (tmp_path / "poetry.lock").write_text("")
    (tmp_path / "pyproject.toml").write_text("[tool]")
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "workflows").mkdir()
    (tmp_path / ".pre-commit-config.yaml").write_text("repos:")

    card = scan(tmp_path)
    recs = get_recommendations(card)
    # Some dimensions should now be satisfied
    assert len(recs) < 7


def test_recs_sorted_by_lowest_score(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Hi")
    card = scan(tmp_path)
    recs = get_recommendations(card)
    scores = [r["current_pct"] for r in recs]
    assert scores == sorted(scores)
