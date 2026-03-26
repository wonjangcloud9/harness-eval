"""Analyzer: Documentation-as-Context quality."""

from pathlib import Path

from harness_eval.analyzers.base import BaseAnalyzer
from harness_eval.models import DimensionScore

DOC_SIGNALS = {
    "readme": ["README.md", "README.rst", "README"],
    "contributing": [
        "CONTRIBUTING.md", "docs/contributing.md",
    ],
    "api_docs": [
        "docs/api.md", "docs/api/", "openapi.yaml",
        "openapi.json", "swagger.json",
    ],
    "changelog": [
        "CHANGELOG.md", "CHANGES.md", "HISTORY.md",
    ],
}


class DocsAnalyzer(BaseAnalyzer):
    """Checks documentation coverage."""

    def analyze(self, project: Path) -> DimensionScore:
        found: list[str] = []
        total = len(DOC_SIGNALS)

        for cat, paths in DOC_SIGNALS.items():
            for p in paths:
                if (project / p).exists():
                    found.append(f"{cat}: {p}")
                    break

        score = len(found) / total if total else 0.0
        if not found:
            found = ["No documentation found"]
        return DimensionScore(
            name="Documentation Quality",
            score=score,
            details=found,
        )
