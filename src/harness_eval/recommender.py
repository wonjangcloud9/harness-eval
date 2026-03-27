"""Recommendation engine based on scorecard."""

from pathlib import Path

from harness_eval.models import DimensionScore, Scorecard

LANG_SPECIFIC: dict[str, dict[str, list[str]]] = {
    "python": {
        "Feedback Loops": [
            "Add ruff.toml or [tool.ruff] in pyproject.toml",
            "Add .pre-commit-config.yaml with ruff hooks",
        ],
        "Reproducibility": [
            "Add uv.lock or poetry.lock for pinned deps",
            "Use pyproject.toml for dependency management",
        ],
    },
    "node": {
        "Feedback Loops": [
            "Add eslint.config.js or .eslintrc",
            "Add .husky/ for pre-commit hooks",
        ],
        "Reproducibility": [
            "Ensure package-lock.json or yarn.lock is committed",
            "Use engines field in package.json for Node version",
        ],
    },
    "go": {
        "Feedback Loops": [
            "Add golangci-lint config (.golangci.yml)",
        ],
        "Reproducibility": [
            "Ensure go.sum is committed",
        ],
    },
    "rust": {
        "Feedback Loops": [
            "Add clippy to CI (cargo clippy)",
            "Add rustfmt.toml for formatting",
        ],
        "Reproducibility": [
            "Ensure Cargo.lock is committed",
        ],
    },
}

RECOMMENDATIONS: dict[str, list[str]] = {
    "Context Engineering": [
        "Add CLAUDE.md with project rules and conventions",
        "Add AGENTS.md or .cursorrules for multi-tool support",
        "Include architecture constraints in context files",
    ],
    "Scaffolding": [
        "Add tool schemas (mcp.json / tools.json)",
        "Create ARCHITECTURE.md with dependency rules",
        "Add PR/issue templates in .github/",
    ],
    "Feedback Loops": [
        "Set up CI with GitHub Actions or similar",
        "Add linter config (ESLint/Ruff/Biome)",
        "Add pre-commit hooks (.pre-commit-config.yaml)",
    ],
    "Safety & Guardrails": [
        "Add Dockerfile for sandboxed execution",
        "Add CODEOWNERS for approval workflow",
        "Add .env.example and secrets scanning",
    ],
    "Reproducibility": [
        "Add Dockerfile for consistent environments",
        "Ensure lockfile exists (poetry.lock, uv.lock)",
        "Pin dependency versions in requirements.txt",
    ],
    "Documentation Quality": [
        "Add README.md with setup and usage",
        "Add CONTRIBUTING.md for contributors",
        "Add CHANGELOG.md to track changes",
    ],
    "Entropy Management": [
        "Keep CLAUDE.md/AGENTS.md under 200 lines",
        "Use repo-relative links, not external URLs",
        "Add ARCHITECTURE.md with layer boundary rules",
        "Add issue refs to TODO/FIXME comments",
        "Validate doc links point to existing files",
    ],
}


def detect_language(project_path: str) -> str:
    """Detect primary project language from file markers."""
    project = Path(project_path)
    markers = {
        "python": ["pyproject.toml", "setup.py", "requirements.txt"],
        "node": ["package.json", "tsconfig.json"],
        "go": ["go.mod"],
        "rust": ["Cargo.toml"],
    }
    for lang, files in markers.items():
        if any((project / f).exists() for f in files):
            return lang
    return "unknown"


def get_recommendations(
    card: Scorecard,
    language: str | None = None,
) -> list[dict]:
    """Return prioritized recommendations, optionally language-specific."""
    if language is None:
        language = detect_language(card.project_path)

    lang_recs = LANG_SPECIFIC.get(language, {})

    results = []
    for dim in card.dimensions:
        if dim.score >= dim.max_score:
            continue
        recs = list(RECOMMENDATIONS.get(dim.name, []))
        recs.extend(lang_recs.get(dim.name, []))
        results.append(
            {
                "dimension": dim.name,
                "current_pct": _pct(dim),
                "suggestions": recs,
            }
        )
    results.sort(key=lambda r: r["current_pct"])
    return results


def _pct(d: DimensionScore) -> float:
    return (d.score / d.max_score * 100) if d.max_score else 0
