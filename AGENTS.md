# agentsmd-lint

## Overview
A linter and scaffolder for AGENTS.md files. Non-obvious: rules are self-registering via the `@rule` decorator in `rules/builtin.py`, so adding a rule requires no wiring elsewhere. The parser is intentionally dependency-free.

## Setup
- Install with dev extras: `pip install -e '.[dev]'`
- Requires: Python 3.10+

## Build
- Build the distribution: `python -m build`

## Testing
- Run the full suite: `pytest -q`
- Run one test: `pytest -q -k "<test_name>"`
- Keep coverage at or above 90%: `pytest --cov=agentsmd_lint`
- All tests must pass before a change is complete.

## Code style
- Format and lint with `ruff format` and `ruff check`.
- Every new rule in `rules/builtin.py` needs a matching test in `tests/test_rules.py`.

## Security
- Never commit secrets or tokens.
- Do not edit files under `dist/` or `*.egg-info/`; they are generated.

## Commit & PR
- Use conventional commits (`feat:`, `fix:`, `docs:`, `test:`).
- Run `pytest -q` and `ruff check` before opening a pull request.
