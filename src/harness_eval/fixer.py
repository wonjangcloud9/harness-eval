"""Auto-fix common harness issues."""

from pathlib import Path


def _detect_language(project: Path) -> str:
    """Detect primary project language."""
    markers = {
        "python": ["pyproject.toml", "setup.py", "requirements.txt"],
        "node": ["package.json", "tsconfig.json"],
        "go": ["go.mod", "go.sum"],
        "rust": ["Cargo.toml"],
        "ruby": ["Gemfile"],
        "java": ["pom.xml", "build.gradle"],
    }
    for lang, files in markers.items():
        if any((project / f).exists() for f in files):
            return lang
    return "unknown"


_GITIGNORE_TEMPLATES: dict[str, str] = {
    "python": (
        "__pycache__/\n*.py[cod]\n*.egg-info/\n" "dist/\nbuild/\n.venv/\n.env\n"
    ),
    "node": "node_modules/\ndist/\n.env\n",
    "go": "vendor/\n",
    "rust": "target/\n",
    "unknown": ".env\n",
}

_CLAUDE_TEMPLATE = (
    "# Project Rules\n\n"
    "## Architecture\n"
    "- Describe layer dependencies here\n\n"
    "## Conventions\n"
    "- Code style and naming rules\n\n"
    "## Security\n"
    "- Approval and access rules\n"
)

_ARCHITECTURE_TEMPLATE = (
    "# Architecture\n\n"
    "## Layer Dependencies\n"
    "```\n"
    "domain -> service -> controller -> api\n"
    "```\n\n"
    "## Rules\n"
    "- Lower layers must not import higher layers\n"
)


def fix_harness(project: Path) -> list[str]:
    """Create missing harness files and return list of actions taken."""
    actions: list[str] = []
    lang = _detect_language(project)

    if not (project / "CLAUDE.md").exists():
        (project / "CLAUDE.md").write_text(_CLAUDE_TEMPLATE)
        actions.append("Created CLAUDE.md")

    if not (project / "ARCHITECTURE.md").exists():
        (project / "ARCHITECTURE.md").write_text(_ARCHITECTURE_TEMPLATE)
        actions.append("Created ARCHITECTURE.md")

    gitignore = project / ".gitignore"
    if not gitignore.exists():
        template = _GITIGNORE_TEMPLATES.get(lang, "")
        gitignore.write_text(template)
        actions.append(f"Created .gitignore ({lang})")

    if not (project / "README.md").exists():
        name = project.name
        (project / "README.md").write_text(f"# {name}\n")
        actions.append("Created README.md")

    if not (project / "CONTRIBUTING.md").exists():
        (project / "CONTRIBUTING.md").write_text(
            "# Contributing\n\n"
            "## Setup\n"
            "1. Clone the repo\n"
            "2. Install dependencies\n"
            "3. Run tests\n"
        )
        actions.append("Created CONTRIBUTING.md")

    if not (project / "CHANGELOG.md").exists():
        (project / "CHANGELOG.md").write_text("# Changelog\n\n## Unreleased\n")
        actions.append("Created CHANGELOG.md")

    if lang == "python":
        pre_commit = project / ".pre-commit-config.yaml"
        if not pre_commit.exists():
            pre_commit.write_text(
                "repos:\n"
                "  - repo: https://github.com/astral-sh/ruff-pre-commit\n"
                "    rev: v0.4.0\n"
                "    hooks:\n"
                "      - id: ruff\n"
                "        args: [--fix]\n"
                "      - id: ruff-format\n"
            )
            actions.append("Created .pre-commit-config.yaml (ruff)")

    return actions
