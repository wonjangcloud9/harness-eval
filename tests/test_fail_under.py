"""Tests for --fail-under CLI flag."""

from click.testing import CliRunner

from harness_eval.cli import main


def test_fail_under_passes_when_above(tmp_path):
    # Create enough harness files to get a non-zero score
    (tmp_path / "CLAUDE.md").write_text("# Rules\n## Architecture\n- layers\n")
    (tmp_path / "README.md").write_text("# Project\nSome docs\n")
    runner = CliRunner()
    result = runner.invoke(main, ["score", str(tmp_path), "--fail-under", "0"])
    assert result.exit_code == 0


def test_fail_under_fails_when_below(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["score", str(tmp_path), "--fail-under", "100"])
    assert result.exit_code == 1
    assert "below threshold" in result.output or result.exit_code == 1
