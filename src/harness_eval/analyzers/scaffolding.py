"""Analyzer: Scaffolding completeness."""

from pathlib import Path

from harness_eval.analyzers.base import BaseAnalyzer
from harness_eval.models import DimensionScore

SCAFFOLDING_SIGNALS = {
    "tool_schemas": [
        "tools.json", "tool_definitions.yaml",
        "mcp.json", ".mcp.json",
    ],
    "arch_constraints": [
        "architecture.md", "ARCHITECTURE.md",
        "docs/architecture.md",
    ],
    "templates": [
        ".github/ISSUE_TEMPLATE",
        ".github/pull_request_template.md",
        "prompts/", "templates/",
    ],
}


class ScaffoldingAnalyzer(BaseAnalyzer):
    """Checks scaffolding artifact presence."""

    def analyze(self, project: Path) -> DimensionScore:
        hits = 0
        total = len(SCAFFOLDING_SIGNALS)
        details: list[str] = []

        for category, paths in SCAFFOLDING_SIGNALS.items():
            for p in paths:
                if (project / p).exists():
                    hits += 1
                    details.append(f"{category}: {p}")
                    break

        score = hits / total if total else 0.0
        if not details:
            details = ["No scaffolding artifacts"]
        return DimensionScore(
            name="Scaffolding",
            score=score,
            details=details,
        )
