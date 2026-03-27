"""Data models for benchmark tasks."""

from dataclasses import dataclass, field


@dataclass
class BenchmarkTask:
    """A single benchmark task extracted from git history."""

    id: str
    description: str
    repo: str
    base_commit: str
    fix_commit: str
    test_patch: str
    files_changed: list[str] = field(default_factory=list)
    hints: list[str] = field(default_factory=list)
    difficulty: str = "medium"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "repo": self.repo,
            "base_commit": self.base_commit,
            "fix_commit": self.fix_commit,
            "test_patch": self.test_patch,
            "files_changed": self.files_changed,
            "hints": self.hints,
            "difficulty": self.difficulty,
        }
