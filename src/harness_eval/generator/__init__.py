"""Benchmark task generation from git history."""

from harness_eval.generator.models import BenchmarkTask
from harness_eval.generator.pipeline import generate_tasks

__all__ = ["BenchmarkTask", "generate_tasks"]
