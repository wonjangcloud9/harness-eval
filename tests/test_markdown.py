"""Tests for markdown reporter."""

from pathlib import Path

from harness_eval.reporters.markdown import render_markdown
from harness_eval.scanner import scan


def test_markdown_contains_grade(tmp_path: Path):
    md = render_markdown(scan(tmp_path))
    assert "Grade F" in md


def test_markdown_has_table(tmp_path: Path):
    md = render_markdown(scan(tmp_path))
    assert "| Dimension |" in md
    assert "Context Engineering" in md


def test_markdown_has_recommendations(tmp_path: Path):
    md = render_markdown(scan(tmp_path))
    assert "## Recommendations" in md
