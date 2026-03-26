"""Tests for init command."""

from pathlib import Path

from click.testing import CliRunner

from harness_eval.cli import main
from harness_eval.init import init_harness


def test_init_creates_files(tmp_path: Path):
    created = init_harness(tmp_path)
    assert "CLAUDE.md" in created
    assert "ARCHITECTURE.md" in created
    assert (tmp_path / "CLAUDE.md").exists()


def test_init_skips_existing(tmp_path: Path):
    (tmp_path / "CLAUDE.md").write_text("custom")
    created = init_harness(tmp_path)
    assert "CLAUDE.md" not in created
    assert (tmp_path / "CLAUDE.md").read_text() == "custom"


def test_init_force_overwrites(tmp_path: Path):
    (tmp_path / "CLAUDE.md").write_text("custom")
    created = init_harness(tmp_path, force=True)
    assert "CLAUDE.md" in created
    assert "custom" not in (tmp_path / "CLAUDE.md").read_text()


def test_init_cli(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(main, ["init", str(tmp_path)])
    assert result.exit_code == 0
    assert "Created" in result.output


def test_init_then_score_improves(tmp_path: Path):
    from harness_eval.scanner import scan

    before = scan(tmp_path).percentage
    init_harness(tmp_path)
    after = scan(tmp_path).percentage
    assert after > before
