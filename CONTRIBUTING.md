# Contributing to CASimation

## Branch workflow

- `main` contains stable, reviewable code.
- Create one branch per change, such as `feature/ahu-formulas` or `fix/vav-electrical-rate`.
- Keep commits focused and use clear messages.
- Run the test suite before merging.

## Local checks

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall app.py estimator
```

## Pull requests

Describe:

1. What changed.
2. Which workbook formulas or business rules were migrated.
3. How the change was validated.
4. Any remaining differences from the workbook.
