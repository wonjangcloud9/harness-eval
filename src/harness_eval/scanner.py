"""Core scanner: runs all analyzers on a project."""

from pathlib import Path

from harness_eval.analyzers.context import ContextAnalyzer
from harness_eval.analyzers.docs import DocsAnalyzer
from harness_eval.analyzers.entropy import EntropyAnalyzer
from harness_eval.analyzers.feedback import FeedbackLoopAnalyzer
from harness_eval.analyzers.reproducibility import (
    ReproducibilityAnalyzer,
)
from harness_eval.analyzers.safety import SafetyAnalyzer
from harness_eval.analyzers.scaffolding import ScaffoldingAnalyzer
from harness_eval.models import Scorecard

ALL_ANALYZERS = [
    ContextAnalyzer(),
    ScaffoldingAnalyzer(),
    FeedbackLoopAnalyzer(),
    SafetyAnalyzer(),
    ReproducibilityAnalyzer(),
    DocsAnalyzer(),
    EntropyAnalyzer(),
]


def scan(project_path: str | Path) -> Scorecard:
    """Scan a project and return its scorecard."""
    project = Path(project_path).resolve()
    if not project.is_dir():
        raise ValueError(f"Not a directory: {project}")

    card = Scorecard(project_path=str(project))
    for analyzer in ALL_ANALYZERS:
        card.dimensions.append(analyzer.analyze(project))
    return card
