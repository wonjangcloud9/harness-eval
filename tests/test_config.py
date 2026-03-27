"""Tests for .harness-eval.yaml config loading."""

import yaml

from harness_eval.config import HarnessConfig, load_config


def test_default_config(tmp_path):
    cfg = load_config(tmp_path)
    assert cfg.is_dimension_enabled("context")
    assert cfg.dimension_weight("scaffolding") == 1.0
    assert cfg.generate.max_tasks == 50


def test_load_config_from_yaml(tmp_path):
    config_data = {
        "dimensions": {
            "context": {"enabled": True, "weight": 2.0},
            "entropy": {"enabled": False},
        },
        "generate": {
            "min_test_lines": 5,
            "max_tasks": 20,
        },
    }
    (tmp_path / ".harness-eval.yaml").write_text(yaml.dump(config_data))
    cfg = load_config(tmp_path)
    assert cfg.dimension_weight("context") == 2.0
    assert not cfg.is_dimension_enabled("entropy")
    assert cfg.generate.min_test_lines == 5
    assert cfg.generate.max_tasks == 20


def test_missing_dimensions_use_defaults(tmp_path):
    (tmp_path / ".harness-eval.yaml").write_text("generate:\n  max_tasks: 10\n")
    cfg = load_config(tmp_path)
    assert cfg.is_dimension_enabled("docs")
    assert cfg.generate.max_tasks == 10


def test_empty_yaml_returns_defaults(tmp_path):
    (tmp_path / ".harness-eval.yaml").write_text("")
    cfg = load_config(tmp_path)
    assert isinstance(cfg, HarnessConfig)
    assert cfg.generate.max_tasks == 50
