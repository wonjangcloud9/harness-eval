"""Tests for CLI commands."""

from click.testing import CliRunner

from harness_eval.cli import main


def test_score_default(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["score", str(tmp_path)])
    assert result.exit_code == 0
    assert "Scorecard" in result.output


def test_score_json(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["score", "--json", str(tmp_path)])
    assert result.exit_code == 0
    assert '"grade"' in result.output


def test_score_markdown(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["score", "--markdown", str(tmp_path)])
    assert result.exit_code == 0
    assert "Grade" in result.output


def test_compare(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (b / "CLAUDE.md").write_text("## Rules\n- test")
    runner = CliRunner()
    result = runner.invoke(main, ["compare", str(a), str(b)])
    assert result.exit_code == 0
    assert "Comparison" in result.output


def test_default_invokes_score(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
