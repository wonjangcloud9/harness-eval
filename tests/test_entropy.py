"""Tests for entropy management analyzer."""

from pathlib import Path

from harness_eval.analyzers.entropy import EntropyAnalyzer


def _analyze(tmp_path: Path):
    return EntropyAnalyzer().analyze(tmp_path)


def test_empty_project_partial_pass(tmp_path: Path):
    result = _analyze(tmp_path)
    # No context files = passes size/url checks
    assert result.score > 0.0


def test_bloated_claude_md(tmp_path: Path):
    (tmp_path / "CLAUDE.md").write_text("line\n" * 250)
    result = _analyze(tmp_path)
    assert "bloated" in " ".join(result.details)


def test_external_urls_flagged(tmp_path: Path):
    (tmp_path / "CLAUDE.md").write_text(
        "Check https://slack.com/channel/foo for info"
    )
    result = _analyze(tmp_path)
    assert "external URL" in " ".join(result.details)


def test_arch_enforcement_detected(tmp_path: Path):
    (tmp_path / "ARCHITECTURE.md").write_text("# Layers")
    result = _analyze(tmp_path)
    assert "architecture enforcement" not in " ".join(
        result.details
    ).lower()


def test_stale_todos(tmp_path: Path):
    code = "# TODO fix this\n" * 10
    (tmp_path / "app.py").write_text(code)
    result = _analyze(tmp_path)
    assert "TODO" in " ".join(result.details)
