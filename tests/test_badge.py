"""Tests for badge generator."""

from pathlib import Path

from harness_eval.reporters.badge import render_badge
from harness_eval.scanner import scan


def test_badge_is_svg(tmp_path: Path):
    svg = render_badge(scan(tmp_path))
    assert svg.startswith("<svg")
    assert "</svg>" in svg


def test_badge_contains_grade(tmp_path: Path):
    svg = render_badge(scan(tmp_path))
    assert "F" in svg  # empty project = F


def test_badge_cli(tmp_path: Path):
    from click.testing import CliRunner

    from harness_eval.cli import main

    runner = CliRunner()
    result = runner.invoke(main, ["badge", str(tmp_path)])
    assert result.exit_code == 0
    assert "<svg" in result.output
