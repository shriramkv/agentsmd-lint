# agentsmd-lint

**A linter and scaffolder for [`AGENTS.md`](https://agents.md) files.** Catch vague, bloated, or low-signal agent instructions before they slow your coding agent down.

[![CI](https://github.com/shriramkv/agentsmd-lint/actions/workflows/ci.yml/badge.svg)](https://github.com/shriramkv/agentsmd-lint/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Why this exists

`AGENTS.md` is the emerging open standard for telling coding agents how to work in your repo : build commands, conventions, test instructions, guardrails. It is now stewarded by the **Agentic AI Foundation (AAIF)** under the Linux Foundation, and read by 30+ tools including Codex, Claude Code, Cursor, Copilot, Gemini CLI, Aider, and Zed.

But there is a catch. The spec has **no required fields by design**, and recent research on 138 real repositories ([Gloaguen et al., 2026](https://asdlc.io/practices/agents-md-spec/)) found that **auto-generated `AGENTS.md` files actually *reduced* agent success rates and inflated cost by ~23%** — mainly by duplicating what the repo already makes obvious, and by giving vague instructions the agent follows literally.

So the problem isn't *schema compliance*. It's **signal density**. `agentsmd-lint` is built around that finding: it doesn't force a rigid structure, it flags the low-value content that makes agents slower and more expensive, and nudges you toward the high-signal sections real repositories converge on.

## Architecture

![agentsmd-lint architecture](assets/architecture.png)

A dependency-free parser feeds a self-registering rule engine; findings flow into a transparent scorer and pretty/JSON reporters that gate CI.

## Install

```bash
pip install agentsmd-lint
```

## Quick start

Lint every `AGENTS.md` in the current tree:

```bash
agentsmd-lint lint .
```

Scaffold a high-signal starter file (that passes its own linter):

```bash
agentsmd-lint init --stack python --name "My Service"
```

List the rules:

```bash
agentsmd-lint rules
```

## Example output

```
AGENTS.md
  ! 12   WARNING  AM020  Vague instruction: 'write good code'. Agents cannot act on this.
       hint: Replace with a concrete, checkable rule (e.g. 'keep functions under 40 lines').
  i 18   INFO     AM021  Section 'About' reads like README prose the agent can already infer.
       hint: Keep only non-obvious, agent-specific context here.
  ! 24   WARNING  AM011  No concrete build/test/run commands found.

  score 79/100  [########--]   0 error(s), 2 warning(s), 1 info
```

## What it checks

| Rule  | Severity | What it catches |
|-------|----------|-----------------|
| AM001 | error    | Empty file or no headings |
| AM002 | warning  | Missing or duplicate H1 title |
| AM010 | warning  | None of the common high-signal sections present |
| AM011 | warning  | No concrete build/test/run commands |
| AM020 | warning  | Vague, unactionable guidance ("write good code") |
| AM021 | info     | Content copied from the README the agent can already infer |
| AM022 | error    | Unedited `/init` output or placeholder text (`TODO`, `TBD`) |
| AM030 | warning  | File exceeds a healthy length budget |
| AM031 | info     | An individual section is too long |
| AM040 | warning  | Empty section |
| AM041 | info     | Bare URL instead of a labelled link |

The **score** is a transparent 0–100: each error costs 20, each warning 7, each info 2. It is a nudge, not a gate — a solid-but-imperfect file still scores well.

## Use in CI

Fail the build if any `AGENTS.md` drops below a quality bar:

```bash
agentsmd-lint lint . --min-score 80
```

### GitHub Action

```yaml
# .github/workflows/agents-lint.yml
name: agents-lint
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install agentsmd-lint
      - run: agentsmd-lint lint . --min-score 80
```

### pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/shriramkv/agentsmd-lint
    rev: v0.1.0
    hooks:
      - id: agentsmd-lint
```

## Configuration

Configure via `[tool.agentsmd-lint]` in `pyproject.toml`, or a standalone `.agentsmd-lint.toml`:

```toml
[tool.agentsmd-lint]
max_words = 1200
min_command_sections = 1
recommended_sections = ["overview", "setup", "test", "security"]
disable = ["AM041"]   # turn off the bare-URL check
```

## Use as a library

```python
from agentsmd_lint import lint_file

result = lint_file("AGENTS.md")
print(result.score, result.ok)
for finding in result.findings:
    print(finding.rule_id, finding.severity, finding.message)
```

## Design principles

- **Signal over schema.** The spec has no required fields; neither does this linter. It optimises for what actually helps agents.
- **Research-backed rules.** The highest-severity rules target the failure modes measured in real studies: duplication, vagueness, and unedited generation.
- **Zero heavy dependencies.** A small, self-contained Markdown parser — fast installs, easy audits.
- **Dogfooded.** This repo's own `AGENTS.md` scores 100/100, checked in CI.

## Contributing

Issues and PRs welcome. New rules live in `src/agentsmd_lint/rules/builtin.py`, each registered with the `@rule` decorator and covered by a test in `tests/`. See `AGENTS.md` for how agents (and humans) should work in this repo.

## License

MIT © shriramkv
