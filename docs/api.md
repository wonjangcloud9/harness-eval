# API Reference

## Python API

### Scanner
```python
from harness_eval.scanner import scan
card = scan("./my-project")
print(card.grade, card.percentage)
```

### Benchmark Generator
```python
from pathlib import Path
from harness_eval.generator import generate_tasks
tasks = generate_tasks(Path("./my-project"))
for task in tasks:
    print(task.id, task.difficulty, task.description)
```

### Remote Repos
```python
from harness_eval.remote import clone_remote, is_remote
if is_remote("user/repo"):
    with clone_remote("user/repo") as local:
        card = scan(str(local))
```

### Configuration
```python
from harness_eval.config import load_config
cfg = load_config(Path("./my-project"))
print(cfg.is_dimension_enabled("entropy"))
print(cfg.generate.max_tasks)
```

### Models
- `Scorecard` — overall result with dimensions list
- `DimensionScore` — single dimension score + details
- `BenchmarkTask` — generated benchmark task with patches
- `pct_to_grade(pct)` — convert percentage to A-F

### Analyzers
All inherit `BaseAnalyzer` with `analyze(Path) -> DimensionScore`.

Available: `ContextAnalyzer`, `ScaffoldingAnalyzer`,
`FeedbackLoopAnalyzer`, `SafetyAnalyzer`,
`ReproducibilityAnalyzer`, `DocsAnalyzer`, `EntropyAnalyzer`

### Reporters
- `print_scorecard(card)` — Rich console output
- `render_markdown(card)` — Markdown string
- `render_badge(card)` — SVG string

## CLI Commands
- `harness-eval score [PATH]` — score a project
- `harness-eval score --fail-under N [PATH]` — CI quality gate
- `harness-eval generate [PATH]` — generate benchmark tasks
- `harness-eval compare <A> <B>` — compare two projects
- `harness-eval badge [PATH]` — generate SVG badge
- `harness-eval init [PATH]` — bootstrap harness files

Paths can be local directories, HTTPS URLs, or GitHub shorthands (`user/repo`).
