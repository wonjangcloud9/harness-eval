"""Analyzer: Context Engineering quality."""

from pathlib import Path

from harness_eval.analyzers.base import BaseAnalyzer
from harness_eval.analyzers.context_depth import score_content_depth
from harness_eval.models import DimensionScore

CONTEXT_FILES = [
    "CLAUDE.md",
    ".claude/CLAUDE.md",
    "AGENTS.md",
    ".github/copilot-instructions.md",
    "GEMINI.md",
    ".cursorrules",
    ".cursor/rules",
    "codex.md",
    "CONVENTIONS.md",
]


class ContextAnalyzer(BaseAnalyzer):
    """Checks context engineering artifacts."""

    def analyze(self, project: Path) -> DimensionScore:
        found = []
        depth_scores: list[float] = []
        for f in CONTEXT_FILES:
            p = project / f
            if p.exists():
                found.append(str(f))
                depth_scores.append(score_content_depth(p))

        if not found:
            return DimensionScore(
                name="Context Engineering",
                score=0.0,
                details=["No context files found"],
            )

        presence = min(len(found) / 2.0, 0.5)
        avg_depth = sum(depth_scores) / len(depth_scores) * 0.5
        score = min(presence + avg_depth, 1.0)
        details = [f"Found: {', '.join(found)}"]
        if avg_depth < 0.15:
            details.append("Content is shallow — add more rules")
        return DimensionScore(
            name="Context Engineering",
            score=score,
            details=details,
        )
