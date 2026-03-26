"""Bootstrap harness engineering files for a project."""

from pathlib import Path

TEMPLATES: dict[str, str] = {
    "CLAUDE.md": (
        "# Project Rules\n\n"
        "## Architecture\n"
        "- Describe layer dependencies here\n\n"
        "## Conventions\n"
        "- Code style and naming rules\n\n"
        "## Security\n"
        "- Approval and access rules\n"
    ),
    "ARCHITECTURE.md": (
        "# Architecture\n\n"
        "## Layer Dependencies\n"
        "```\n"
        "domain -> service -> controller -> api\n"
        "```\n\n"
        "## Rules\n"
        "- Lower layers must not import higher layers\n"
    ),
    ".gitignore": (
        "__pycache__/\n*.py[cod]\n*.egg-info/\n"
        "dist/\nbuild/\n.venv/\n.env\nnode_modules/\n"
    ),
}


def init_harness(
    project: Path,
    force: bool = False,
) -> list[str]:
    """Create missing harness files. Returns created list."""
    created: list[str] = []
    for name, content in TEMPLATES.items():
        target = project / name
        if target.exists() and not force:
            continue
        target.write_text(content)
        created.append(name)
    return created
