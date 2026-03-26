"""Analyzer: Reproducibility index."""

from pathlib import Path

from harness_eval.analyzers.base import BaseAnalyzer
from harness_eval.models import DimensionScore

REPRO_SIGNALS = {
    "containerization": [
        "Dockerfile", "docker-compose.yml",
        "docker-compose.yaml",
    ],
    "lockfile": [
        "poetry.lock", "uv.lock", "Pipfile.lock",
        "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
        "Cargo.lock", "go.sum",
    ],
    "pinned_deps": [
        "requirements.txt", "constraints.txt",
    ],
}


class ReproducibilityAnalyzer(BaseAnalyzer):
    """Checks environment reproducibility."""

    def analyze(self, project: Path) -> DimensionScore:
        found: list[str] = []
        total = len(REPRO_SIGNALS)

        for cat, paths in REPRO_SIGNALS.items():
            for p in paths:
                if (project / p).exists():
                    found.append(f"{cat}: {p}")
                    break

        score = len(found) / total if total else 0.0
        if not found:
            found = ["No reproducibility signals"]
        return DimensionScore(
            name="Reproducibility",
            score=score,
            details=found,
        )
