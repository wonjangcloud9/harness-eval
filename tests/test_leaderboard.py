"""Tests for leaderboard command."""

from click.testing import CliRunner

from harness_eval.cli import main


def test_leaderboard_ranks_projects(tmp_path):
    a = tmp_path / "project_a"
    b = tmp_path / "project_b"
    a.mkdir()
    b.mkdir()
    (a / "CLAUDE.md").write_text("# Rules\n## Arch\n- layers\n")
    (a / "README.md").write_text("# Project A\n")

    runner = CliRunner()
    result = runner.invoke(main, ["leaderboard", str(a), str(b)])
    assert result.exit_code == 0
    assert "Leaderboard" in result.output


def test_leaderboard_json(tmp_path):
    a = tmp_path / "project_a"
    a.mkdir()
    runner = CliRunner()
    result = runner.invoke(main, ["leaderboard", str(a), "--json"])
    assert result.exit_code == 0
    assert '"rank"' in result.output
    assert '"grade"' in result.output
