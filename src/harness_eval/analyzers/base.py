"""Base analyzer interface."""

from abc import ABC, abstractmethod
from pathlib import Path

from harness_eval.models import DimensionScore


class BaseAnalyzer(ABC):
    """All dimension analyzers inherit this."""

    @abstractmethod
    def analyze(self, project: Path) -> DimensionScore:
        ...
