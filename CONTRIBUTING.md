# Contributing to harness-eval

## Setup
```bash
git clone https://github.com/wonjangcloud9/harness-eval
cd harness-eval
python3 -m venv .venv && source .venv/bin/activate
pip install -e . pytest
```

## Adding an Analyzer
1. Create `src/harness_eval/analyzers/your_name.py`
2. Inherit `BaseAnalyzer`, implement `analyze()`
3. Register in `scanner.py` → `ALL_ANALYZERS`
4. Add tests in `tests/test_your_name.py`
5. Add recommendations in `recommender.py`

## Running Tests
```bash
pytest tests/ -v
```

## Pull Requests
- One feature per PR
- All tests must pass
- Include test for new analyzers
