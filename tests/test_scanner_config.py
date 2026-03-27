"""Tests for scanner with .harness-eval.yaml config integration."""

import yaml

from harness_eval.scanner import scan


def test_disabled_dimension_excluded(tmp_path):
    config = {"dimensions": {"entropy": {"enabled": False}}}
    (tmp_path / ".harness-eval.yaml").write_text(yaml.dump(config))
    card = scan(tmp_path)
    names = [d.name for d in card.dimensions]
    assert "Entropy Management" not in names


def test_weighted_dimension(tmp_path):
    config = {"dimensions": {"context": {"weight": 2.0}}}
    (tmp_path / ".harness-eval.yaml").write_text(yaml.dump(config))
    card = scan(tmp_path)
    ctx = next(d for d in card.dimensions if "context" in d.name.lower())
    assert ctx.max_score == 2.0


def test_default_config_all_dimensions(tmp_path):
    card = scan(tmp_path)
    assert len(card.dimensions) == 7
