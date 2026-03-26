# harness-eval

[![CI](https://github.com/wonjangcloud9/harness-eval/actions/workflows/ci.yml/badge.svg)](https://github.com/wonjangcloud9/harness-eval/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Open-source CLI tool that measures **harness engineering** quality in your projects.

Harness engineering = the infrastructure around AI coding agents (Claude Code, Codex, Copilot, Cursor) that determines agent performance. Same model, better harness = dramatically better results.

## Quick Start

```bash
pip install harness-eval

# Score your project
harness-eval score .

# Bootstrap harness files
harness-eval init .

# Compare two projects
harness-eval compare ./project-a ./project-b
```

## Dimensions Scored (7)

| Dimension | What it checks |
|-----------|---------------|
| Context Engineering | CLAUDE.md, AGENTS.md, .cursorrules + content depth |
| Scaffolding | Tool schemas, architecture docs, templates |
| Feedback Loops | CI/CD, linters, pre-commit hooks |
| Safety & Guardrails | Sandbox, approval workflow, secrets protection |
| Reproducibility | Containers, lockfiles, pinned dependencies |
| Documentation | README, CONTRIBUTING, CHANGELOG, API docs |
| Entropy Management | Config drift, stale TODOs, doc-code sync |

## Output Formats

```bash
harness-eval score .              # Rich console table
harness-eval score --json .       # JSON (CI-friendly)
harness-eval score --markdown .   # Markdown (PR comments)
harness-eval badge -o badge.svg . # SVG badge
```

## GitHub Action

Add to `.github/workflows/harness-eval.yml`:

```yaml
- run: pip install harness-eval
- run: harness-eval score --markdown . > score.md
- uses: marocchino/sticky-pull-request-comment@v2
  with:
    path: score.md
```

## Development

```bash
git clone https://github.com/wonjangcloud9/harness-eval.git
cd harness-eval
python3 -m venv .venv && source .venv/bin/activate
pip install -e . pytest
pytest tests/ -v
```

## License

MIT
