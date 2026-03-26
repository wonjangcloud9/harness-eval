"""Analyzer: Context Engineering quality."""

from pathlib import Path

from harness_eval.analyzers.base import BaseAnalyzer
from harness_eval.models import DimensionScore

CONTEXT_FILES = [
    "CLAUDE.md", ".claude/CLAUDE.md",
    "AGENTS.md", ".github/copilot-instructions.md",
    "GEMINI.md", ".cursorrules", ".cursor/rules",
    "codex.md", "CONVENTIONS.md",
]


class ContextAnalyzer(BaseAnalyzer):
    """Checks context engineering artifacts."""

    def analyze(self, project: Path) -> DimensionScore:
        found = []
        for f in CONTEXT_FILES:
            p = project / f
            if p.exists():
                found.append(str(f))

        score = min(len(found) / 2.0, 1.0)
        details = (
            [f"Found: {', '.join(found)}"]
            if found
            else ["No context files found"]
        )
        return DimensionScore(
            name="Context Engineering",
            score=score,
            details=details,
        )
