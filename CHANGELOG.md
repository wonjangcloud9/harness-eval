# Changelog

## 0.2.0 (2026-03-27)

### Added
- `harness-eval generate` — create SWE-bench-style benchmark tasks from git history
- Remote URL support — score/generate with GitHub URLs or `user/repo` shorthand
- `.harness-eval.yaml` config — toggle dimensions, set weights, configure generation
- `--fail-under N` flag — CI quality gate, exit 1 if score below threshold
- 18 new tests (55 total)

## 0.1.0 (2026-03-27)

### Added
- Initial release
- 6-dimension harness quality scanner
- Rich console output with color-coded scores
- JSON and Markdown output formats
- Recommendation engine with prioritized suggestions
- Letter grade system (A-F)
- Compare mode for two projects
- Content depth analysis for context files
- GitHub Actions CI (Python 3.11-3.13)
