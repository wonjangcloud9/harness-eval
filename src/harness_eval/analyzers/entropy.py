"""Analyzer: Entropy Management quality.

Detects config drift, doc-code sync issues,
and stale artifacts that degrade agent performance.
"""

import re
from pathlib import Path

from harness_eval.analyzers.base import BaseAnalyzer
from harness_eval.models import DimensionScore

EXTERNAL_URL_RE = re.compile(r"https?://(?!github\.com/)[^\s\)>\"']+")
TODO_NO_REF_RE = re.compile(
    r"#\s*(TODO|FIXME|HACK|XXX)\b(?!.*(?:#\d|issue|ticket))",
    re.IGNORECASE,
)


class EntropyAnalyzer(BaseAnalyzer):
    """Checks entropy management signals."""

    def analyze(self, project: Path) -> DimensionScore:
        checks: list[tuple[str, bool]] = []
        details: list[str] = []

        # 1. Context file size (not bloated)
        checks.append(self._check_context_size(project, details))
        # 2. No external URLs in agent docs
        checks.append(self._check_external_urls(project, details))
        # 3. Doc links point to existing files
        checks.append(self._check_doc_links(project, details))
        # 4. Stale TODOs without issue refs
        checks.append(self._check_stale_todos(project, details))
        # 5. Arch boundary config exists
        checks.append(self._check_arch_enforcement(project, details))

        passed = sum(1 for _, ok in checks if ok)
        score = passed / len(checks) if checks else 0.0

        if not details:
            details = ["Good entropy management"]
        return DimensionScore(
            name="Entropy Management",
            score=score,
            details=details,
        )

    def _check_context_size(
        self, project: Path, details: list[str]
    ) -> tuple[str, bool]:
        for name in ["CLAUDE.md", "AGENTS.md", "CONVENTIONS.md"]:
            p = project / name
            if p.exists():
                lines = p.read_text(errors="ignore").splitlines()
                if len(lines) > 200:
                    details.append(f"{name}: {len(lines)} lines (bloated)")
                    return ("context_size", False)
        return ("context_size", True)

    def _check_external_urls(
        self, project: Path, details: list[str]
    ) -> tuple[str, bool]:
        for name in ["CLAUDE.md", "AGENTS.md"]:
            p = project / name
            if p.exists():
                text = p.read_text(errors="ignore")
                urls = EXTERNAL_URL_RE.findall(text)
                if urls:
                    details.append(f"{name}: {len(urls)} external URL(s)")
                    return ("external_urls", False)
        return ("external_urls", True)

    def _check_doc_links(self, project: Path, details: list[str]) -> tuple[str, bool]:
        docs_dir = project / "docs"
        if not docs_dir.is_dir():
            return ("doc_links", True)  # no docs to check

        broken = 0
        for md in docs_dir.rglob("*.md"):
            text = md.read_text(errors="ignore")
            for m in re.finditer(r"\[.*?\]\(([^http][^\)]+)\)", text):
                ref = m.group(1).split("#")[0]
                if ref and not (md.parent / ref).exists():
                    broken += 1
        if broken:
            details.append(f"docs: {broken} broken link(s)")
            return ("doc_links", False)
        return ("doc_links", True)

    def _check_stale_todos(self, project: Path, details: list[str]) -> tuple[str, bool]:
        stale = 0
        for ext in ("*.py", "*.ts", "*.js", "*.go", "*.rs"):
            for f in project.rglob(ext):
                if ".venv" in str(f) or "node_modules" in str(f):
                    continue
                try:
                    text = f.read_text(errors="ignore")
                except OSError:
                    continue
                stale += len(TODO_NO_REF_RE.findall(text))
        if stale > 5:
            details.append(f"{stale} TODOs without issue refs")
            return ("stale_todos", False)
        return ("stale_todos", True)

    def _check_arch_enforcement(
        self, project: Path, details: list[str]
    ) -> tuple[str, bool]:
        signals = [
            ".importlinter",
            "pyproject.toml",  # [tool.import-linter]
            "ARCHITECTURE.md",
            "docs/architecture.md",
        ]
        for s in signals:
            p = project / s
            if p.exists():
                if s == "pyproject.toml":
                    text = p.read_text(errors="ignore")
                    if "import-linter" in text or "import_linter" in text:
                        return ("arch_enforcement", True)
                    continue
                return ("arch_enforcement", True)
        details.append("No architecture enforcement config")
        return ("arch_enforcement", False)
