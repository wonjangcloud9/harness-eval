"""Recommendation engine based on scorecard."""

from harness_eval.models import DimensionScore, Scorecard

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


def get_recommendations(card: Scorecard) -> list[dict]:
    """Return prioritized recommendations."""
    results = []
    for dim in card.dimensions:
        if dim.score >= dim.max_score:
            continue
        recs = RECOMMENDATIONS.get(dim.name, [])
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
