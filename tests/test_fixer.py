"""Tests for harness-eval fix command."""

from click.testing import CliRunner

from harness_eval.cli import main
from harness_eval.fixer import fix_harness


def test_fix_creates_missing_files(tmp_path):
    actions = fix_harness(tmp_path)
    assert len(actions) >= 4
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / "ARCHITECTURE.md").exists()
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / ".gitignore").exists()


def test_fix_skips_existing(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("existing")
    actions = fix_harness(tmp_path)
    assert not any("CLAUDE.md" in a for a in actions)
    assert (tmp_path / "CLAUDE.md").read_text() == "existing"


def test_fix_detects_python(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    actions = fix_harness(tmp_path)
    assert any(".pre-commit" in a for a in actions)


def test_fix_cli(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["fix", str(tmp_path)])
    assert result.exit_code == 0
    assert "fix(es) applied" in result.output


def test_fix_cli_nothing_to_fix(tmp_path):
    fix_harness(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["fix", str(tmp_path)])
    assert result.exit_code == 0
    assert "Nothing to fix" in result.output
