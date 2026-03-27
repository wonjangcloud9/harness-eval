# Benchmark Generation & UX Improvements Design

## Problem
harness-eval scores repos but can't generate benchmarks from them.
Users want to create SWE-bench-style tasks from any repo automatically.

## New Features

### 1. `harness-eval generate <path-or-url>`
Analyze git history to extract benchmark tasks:
- Find bug-fix commits (message contains fix/bug/close + has test changes)
- Extract before/after state (base commit + fix patch)
- Generate YAML task files with description, base_commit, test_patch

### 2. Remote URL support
`harness-eval score https://github.com/user/repo`
- Auto clone to temp dir, score, cleanup

### 3. `.harness-eval.yaml` config
```yaml
dimensions:
  context: {enabled: true, weight: 1.0}
  scaffolding: {enabled: true, weight: 1.0}
generate:
  min_test_lines: 3
  max_tasks: 50
```

### 4. `--fail-under N` flag
Exit code 1 when score < threshold. For CI gates.

## Architecture

```
src/harness_eval/
├── generator/
│   ├── __init__.py
│   ├── git_analyzer.py    # Parse git log for fix commits
│   ├── task_extractor.py  # Build benchmark tasks from commits
│   └── models.py          # BenchmarkTask dataclass
├── remote.py              # Clone remote URLs to temp
├── config.py              # Load .harness-eval.yaml
└── cli.py                 # Add generate, --fail-under
```

## Data Flow
1. User runs `harness-eval generate ./my-repo`
2. git_analyzer scans log for fix commits with test changes
3. task_extractor creates BenchmarkTask for each valid commit
4. Output: `benchmarks/` dir with YAML task files

## BenchmarkTask Schema
```yaml
id: "fix-auth-token-001"
description: "Fix token refresh race condition"
repo: "https://github.com/user/repo"
base_commit: "abc123"
test_patch: |
  diff --git a/tests/test_auth.py ...
hints:
  - "Check token expiry logic in auth/token.py"
files_changed:
  - "src/auth/token.py"
difficulty: "medium"
```

## Implementation Order
1. config.py + .harness-eval.yaml support
2. --fail-under flag
3. remote.py (URL clone support)
4. generator/ (git_analyzer → task_extractor → models)
5. CLI generate command
6. Tests for everything
7. Docs update
