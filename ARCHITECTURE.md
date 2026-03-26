# Architecture

## Layer Dependency Rules

```
models.py          (0 - no internal imports)
  ↑
analyzers/base.py  (1 - imports models)
  ↑
analyzers/*        (2 - imports base + models)
  ↑
scanner.py         (3 - imports all analyzers)
recommender.py     (3 - imports models)
  ↑
reporters/*        (4 - imports models + recommender)
  ↑
cli.py             (5 - imports scanner + reporters)
```

## Rules
- Lower layers MUST NOT import higher layers
- Analyzers must not import other analyzers
- Reporters must not import analyzers directly
- CLI is the only entry point
