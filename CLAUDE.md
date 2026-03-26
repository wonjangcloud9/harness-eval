# harness-eval Project Rules

## Architecture
- Analyzers in `src/harness_eval/analyzers/`
- Each analyzer: one file, one class, inherits `BaseAnalyzer`
- Reporters in `src/harness_eval/reporters/`
- Models in `models.py`, scanner in `scanner.py`

## Conventions
- Python 3.11+, type hints required
- Test every analyzer and reporter
- Use `pytest` with `tmp_path` fixture
- Format: Black 88, lint: Ruff (F,E,I,N)
- Dependencies: click, rich, pyyaml only

## Security
- Never execute user code during analysis
- Read-only filesystem access for scanning
- No network calls in analyzers
