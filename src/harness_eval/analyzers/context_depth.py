"""Deep content analysis for context files."""

from pathlib import Path

QUALITY_KEYWORDS = [
    "architecture", "convention", "rule",
    "dependency", "constraint", "pattern",
    "test", "lint", "format", "style",
    "security", "permission", "approval",
    "tool", "mcp", "agent", "prompt",
]


def score_content_depth(file_path: Path) -> float:
    """Score a context file's content quality 0-1."""
    if not file_path.exists():
        return 0.0
    text = file_path.read_text(errors="ignore").lower()
    if not text.strip():
        return 0.1  # exists but empty

    length_score = min(len(text) / 2000, 0.4)
    keyword_hits = sum(1 for k in QUALITY_KEYWORDS if k in text)
    keyword_score = min(keyword_hits / 8, 0.4)
    has_structure = any(
        marker in text
        for marker in ["## ", "- ", "* ", "1. "]
    )
    structure_score = 0.2 if has_structure else 0.0

    return min(length_score + keyword_score + structure_score, 1.0)
