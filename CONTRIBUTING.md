# Contributing to agentsmd-lint

Thanks for helping improve `AGENTS.md` quality across the ecosystem.

## Development setup

```bash
git clone https://github.com/shriramkv/agentsmd-lint
cd agentsmd-lint
pip install -e '.[dev]'
pytest -q
```

## Adding a rule

1. Add a function in `src/agentsmd_lint/rules/builtin.py` decorated with
   `@rule("AMxxx", "one-line summary")`. It receives a `Document` and a
   `RuleConfig` and yields `Finding` objects.
2. Choose the severity deliberately: `ERROR` for things that will break an
   agent run, `WARNING` for quality issues, `INFO` for gentle nudges.
3. Add tests in `tests/test_rules.py` covering both the firing and the
   non-firing case.
4. Document the rule in the README table.
5. Run `pytest -q` and `ruff check src tests`.

## Rule design philosophy

`AGENTS.md` has no required fields. Rules should optimise for **signal
density** — flag content that measurably slows agents down (duplication,
vagueness, unedited generation) rather than enforcing a rigid schema.

## Reporting issues

Use GitHub Issues. Include the `AGENTS.md` snippet, the output you got, and
what you expected.
