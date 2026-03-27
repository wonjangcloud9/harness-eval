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
from harness_eval.config import HarnessConfig, load_config
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


def scan(
    project_path: str | Path,
    config: HarnessConfig | None = None,
) -> Scorecard:
    """Scan a project and return its scorecard."""
    project = Path(project_path).resolve()
    if not project.is_dir():
        raise ValueError(f"Not a directory: {project}")

    if config is None:
        config = load_config(project)

    card = Scorecard(project_path=str(project))
    for analyzer in ALL_ANALYZERS:
        dim = analyzer.analyze(project)
        if not config.is_dimension_enabled(dim.name):
            continue
        weight = config.dimension_weight(dim.name)
        dim.score *= weight
        dim.max_score *= weight
        card.dimensions.append(dim)
    return card
