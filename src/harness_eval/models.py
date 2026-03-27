"""Score models for harness evaluation."""

from dataclasses import dataclass, field


@dataclass
class DimensionScore:
    name: str
    score: float  # 0.0 ~ 1.0
    max_score: float = 1.0
    details: list[str] = field(default_factory=list)


@dataclass
class Scorecard:
    project_path: str
    dimensions: list[DimensionScore] = field(default_factory=list)

    @property
    def total(self) -> float:
        if not self.dimensions:
            return 0.0
        return sum(d.score for d in self.dimensions)

    @property
    def max_total(self) -> float:
        return sum(d.max_score for d in self.dimensions)

    @property
    def percentage(self) -> float:
        if self.max_total == 0:
            return 0.0
        return (self.total / self.max_total) * 100

    @property
    def grade(self) -> str:
        return pct_to_grade(self.percentage)


def pct_to_grade(pct: float) -> str:
    """Convert percentage to letter grade."""
    if pct >= 90:
        return "A"
    if pct >= 75:
        return "B"
    if pct >= 55:
        return "C"
    if pct >= 35:
        return "D"
    return "F"
