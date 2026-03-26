# API Reference

## Python API

### Scanner
```python
from harness_eval.scanner import scan
card = scan("./my-project")
print(card.grade, card.percentage)
```

### Models
- `Scorecard` — overall result with dimensions list
- `DimensionScore` — single dimension score + details
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
- `harness-eval compare <A> <B>` — compare two projects
- `harness-eval badge [PATH]` — generate SVG badge
- `harness-eval init [PATH]` — bootstrap harness files
