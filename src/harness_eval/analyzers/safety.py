"""Analyzer: Safety & guardrail coverage."""

from pathlib import Path

from harness_eval.analyzers.base import BaseAnalyzer
from harness_eval.models import DimensionScore

SAFETY_SIGNALS = {
    "sandbox": [
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        ".devcontainer/",
    ],
    "approval": [
        "CODEOWNERS",
        ".github/CODEOWNERS",
        ".github/workflows",  # PR checks
    ],
    "secrets_guard": [
        ".gitignore",
        ".env.example",
        ".gitleaks.toml",
        ".secretlintrc",
    ],
}


class SafetyAnalyzer(BaseAnalyzer):
    """Checks safety and guardrail layers."""

    def analyze(self, project: Path) -> DimensionScore:
        found: list[str] = []
        total = len(SAFETY_SIGNALS)

        for category, paths in SAFETY_SIGNALS.items():
            for p in paths:
                if (project / p).exists():
                    found.append(f"{category}: {p}")
                    break

        score = len(found) / total if total else 0.0
        if not found:
            found = ["No safety signals"]
        return DimensionScore(
            name="Safety & Guardrails",
            score=score,
            details=found,
        )
