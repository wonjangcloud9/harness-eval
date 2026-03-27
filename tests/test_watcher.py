"""Tests for watch functionality."""

from harness_eval.watcher import _get_mtimes


def test_get_mtimes_empty_project(tmp_path):
    mtimes = _get_mtimes(tmp_path)
    assert mtimes == {}


def test_get_mtimes_detects_files(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("# Rules")
    (tmp_path / "README.md").write_text("# Project")
    mtimes = _get_mtimes(tmp_path)
    assert len(mtimes) == 2


def test_get_mtimes_detects_dirs(tmp_path):
    gh = tmp_path / ".github" / "workflows"
    gh.mkdir(parents=True)
    (gh / "ci.yml").write_text("name: CI")
    mtimes = _get_mtimes(tmp_path)
    assert len(mtimes) == 1
    assert any("ci.yml" in k for k in mtimes)
