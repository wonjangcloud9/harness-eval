# harness-eval

Open-source CLI tool that measures **harness engineering** quality in your projects.

Harness engineering = the infrastructure around AI coding agents (Claude Code, Codex, Copilot, Cursor) that determines agent performance. Same model, better harness → dramatically better results.

## Install

```bash
pip install harness-eval
```

## Usage

```bash
# Scan current directory
harness-eval .

# JSON output
harness-eval --json .

# Without recommendations
harness-eval --no-recommend .
```

## Dimensions Scored

| Dimension | What it checks |
|-----------|---------------|
| Context Engineering | CLAUDE.md, AGENTS.md, .cursorrules + content depth |
| Scaffolding | Tool schemas, architecture docs, templates |
| Feedback Loops | CI/CD, linters, pre-commit hooks |
| Safety & Guardrails | Sandbox, approval workflow, secrets protection |
| Reproducibility | Containers, lockfiles, pinned dependencies |
| Documentation | README, CONTRIBUTING, CHANGELOG, API docs |

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
