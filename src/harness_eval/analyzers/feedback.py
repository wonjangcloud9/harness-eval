"""Analyzer: Feedback loop maturity."""

from pathlib import Path

from harness_eval.analyzers.base import BaseAnalyzer
from harness_eval.models import DimensionScore

CI_SIGNALS = [
    ".github/workflows",
    ".gitlab-ci.yml",
    "Jenkinsfile",
    ".circleci/config.yml",
]

LINT_SIGNALS = [
    ".eslintrc",
    ".eslintrc.js",
    ".eslintrc.json",
    "pyproject.toml",
    "setup.cfg",  # ruff/flake8
    ".prettierrc",
    ".prettierrc.json",
    "biome.json",
]

HOOK_SIGNALS = [
    ".husky/",
    ".pre-commit-config.yaml",
    ".github/hooks/",
]


class FeedbackLoopAnalyzer(BaseAnalyzer):
    """Checks CI, linter, and hook integration."""

    def analyze(self, project: Path) -> DimensionScore:
        found: list[str] = []

        for p in CI_SIGNALS:
            if (project / p).exists():
                found.append(f"CI: {p}")
                break

        for p in LINT_SIGNALS:
            if (project / p).exists():
                found.append(f"Lint: {p}")
                break

        for p in HOOK_SIGNALS:
            if (project / p).exists():
                found.append(f"Hooks: {p}")
                break

        score = len(found) / 3.0
        if not found:
            found = ["No feedback loops detected"]
        return DimensionScore(
            name="Feedback Loops",
            score=score,
            details=found,
        )
