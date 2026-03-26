"""Tests for context content depth scoring."""

from pathlib import Path

from harness_eval.analyzers.context_depth import score_content_depth


def test_missing_file(tmp_path: Path):
    score = score_content_depth(tmp_path / "nope.md")
    assert score == 0.0


def test_empty_file(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text("")
    assert score_content_depth(f) == 0.1


def test_rich_content_scores_higher(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text(
        "## Architecture\n"
        "- Follow convention for testing\n"
        "- Use dependency injection pattern\n"
        "- Security rules: approval required\n"
        "- Lint with ruff, format with black\n"
        "- Tool definitions in mcp.json\n"
        "- Agent prompt constraints\n"
    )
    score = score_content_depth(f)
    assert score > 0.5


def test_shallow_content_scores_low(tmp_path: Path):
    f = tmp_path / "CLAUDE.md"
    f.write_text("hello")
    score = score_content_depth(f)
    assert score < 0.3
