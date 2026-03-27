# harness-eval

[![CI](https://github.com/wonjangcloud9/harness-eval/actions/workflows/ci.yml/badge.svg)](https://github.com/wonjangcloud9/harness-eval/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Open-source CLI tool that measures **harness engineering** quality and **generates benchmarks** from any repository.

Harness engineering = the infrastructure around AI coding agents (Claude Code, Codex, Copilot, Cursor) that determines agent performance. Same model, better harness = dramatically better results.

## Quick Start

```bash
pip install harness-eval

# Score your project
harness-eval score .

# Score a remote repo (GitHub URL or shorthand)
harness-eval score user/repo

# Generate benchmark tasks from git history
harness-eval generate .

# Bootstrap harness files
harness-eval init .

# Compare two projects
harness-eval compare ./project-a ./project-b
```

## Commands

### `score` — Measure harness quality

```bash
harness-eval score .                          # Rich console table
harness-eval score --json .                   # JSON (CI-friendly)
harness-eval score --markdown .               # Markdown (PR comments)
harness-eval score --fail-under 70 .          # Exit 1 if below 70%
harness-eval score https://github.com/u/repo  # Score remote repo
harness-eval score user/repo                  # GitHub shorthand
```

### `generate` — Create benchmarks from any repo

Extract SWE-bench-style tasks from a repo's git history automatically:

```bash
harness-eval generate .                       # Local repo
harness-eval generate user/repo               # Remote repo
harness-eval generate . --max-tasks 20        # Limit tasks
harness-eval generate . --json                # JSON output
harness-eval generate . -o my-benchmarks/     # Custom output dir
```

How it works:
1. Scans git log for **bug-fix commits** (messages with fix/bug/close/resolve)
2. Filters for commits that have **both source and test changes**
3. Extracts the **test patch** as the verification criteria
4. Generates YAML task files with base commit, test patch, hints, difficulty

### `leaderboard` — Rank multiple projects

```bash
harness-eval leaderboard ./proj-a ./proj-b ./proj-c
harness-eval leaderboard user/repo-a user/repo-b --json
```

### `run` — Execute benchmark tasks

```bash
harness-eval run . -t benchmarks/      # Run tasks against local repo
harness-eval run . --json              # JSON output for CI
```

Validates that generated benchmark tasks are correct by checking
that test patches catch the bugs on the base commit.

### `fix` — Auto-fix harness issues

```bash
harness-eval fix .           # Create missing CLAUDE.md, ARCHITECTURE.md, etc.
```

Detects your project language (Python/Node/Go/Rust) and creates
language-appropriate files (.pre-commit-config.yaml for Python, etc.)

### `explain` — Learn about dimensions

```bash
harness-eval explain           # Show all dimensions
harness-eval explain context   # Explain one dimension
```

### `badge` — SVG score badge

```bash
harness-eval badge -o badge.svg .
```

### `init` — Bootstrap harness files

```bash
harness-eval init .          # Create CLAUDE.md, ARCHITECTURE.md, .gitignore
harness-eval init . --force  # Overwrite existing
```

### `compare` — Side-by-side comparison

```bash
harness-eval compare ./project-a ./project-b
harness-eval compare user/repo-a user/repo-b  # Remote repos too
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

## Configuration

Create `.harness-eval.yaml` in your project root:

```yaml
dimensions:
  context: {enabled: true, weight: 2.0}    # Double context weight
  entropy: {enabled: false}                 # Disable entropy checks
generate:
  min_test_lines: 3      # Minimum test lines for a valid task
  max_tasks: 50           # Maximum benchmark tasks to generate
  include_merge_commits: false
```

## CI Integration

### GitHub Action

```yaml
- run: pip install harness-eval
- run: harness-eval score --fail-under 70 --markdown . > score.md
- uses: marocchino/sticky-pull-request-comment@v2
  with:
    path: score.md
```

### Quality Gate

```bash
# Fail CI if harness quality drops below threshold
harness-eval score --fail-under 70 .
```

## Development

```bash
git clone https://github.com/wonjangcloud9/harness-eval.git
cd harness-eval
python3 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ -v
```

## License

MIT
