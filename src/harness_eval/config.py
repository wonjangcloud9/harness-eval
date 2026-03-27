"""Load project-level .harness-eval.yaml configuration."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

CONFIG_FILENAME = ".harness-eval.yaml"

DEFAULT_DIMENSIONS: dict[str, dict] = {
    "context": {"enabled": True, "weight": 1.0},
    "scaffolding": {"enabled": True, "weight": 1.0},
    "feedback": {"enabled": True, "weight": 1.0},
    "safety": {"enabled": True, "weight": 1.0},
    "reproducibility": {"enabled": True, "weight": 1.0},
    "docs": {"enabled": True, "weight": 1.0},
    "entropy": {"enabled": True, "weight": 1.0},
}


@dataclass
class GenerateConfig:
    min_test_lines: int = 3
    max_tasks: int = 50
    include_merge_commits: bool = False


@dataclass
class HarnessConfig:
    dimensions: dict[str, dict] = field(
        default_factory=lambda: dict(DEFAULT_DIMENSIONS)
    )
    generate: GenerateConfig = field(default_factory=GenerateConfig)

    def is_dimension_enabled(self, name: str) -> bool:
        key = name.lower().split()[0]
        dim = self.dimensions.get(key, {"enabled": True})
        return dim.get("enabled", True)

    def dimension_weight(self, name: str) -> float:
        key = name.lower().split()[0]
        dim = self.dimensions.get(key, {"weight": 1.0})
        return dim.get("weight", 1.0)


def load_config(project: Path) -> HarnessConfig:
    """Load config from .harness-eval.yaml or return defaults."""
    config_path = project / CONFIG_FILENAME
    if not config_path.exists():
        return HarnessConfig()

    raw = yaml.safe_load(config_path.read_text()) or {}
    dims = dict(DEFAULT_DIMENSIONS)
    if "dimensions" in raw:
        for key, val in raw["dimensions"].items():
            if isinstance(val, dict):
                dims[key] = {**dims.get(key, {}), **val}
    gen_raw = raw.get("generate", {})
    gen = GenerateConfig(
        min_test_lines=gen_raw.get("min_test_lines", 3),
        max_tasks=gen_raw.get("max_tasks", 50),
        include_merge_commits=gen_raw.get("include_merge_commits", False),
    )
    return HarnessConfig(dimensions=dims, generate=gen)
