import json

from agentsmd_lint import lint_text
from agentsmd_lint.cli import main
from agentsmd_lint.scaffold import render


GOOD = """# Acme API

## Overview
Non-obvious: auth tokens are minted by the sidecar, not the app.

## Setup
- Install: `pip install -e '.[dev]'`
- Requires: Python 3.11+

## Testing
- Run all: `pytest -q`
- Single: `pytest -q -k "<name>"`

## Code style
- Format with `ruff format`.

## Security
- Never modify `migrations/` without instruction.

## Commit & PR
- Conventional commits; run `pytest -q` before a PR.
"""


def test_good_file_scores_high_and_passes():
    r = lint_text("AGENTS.md", GOOD)
    assert r.ok
    assert r.score >= 90


def test_score_decreases_with_problems():
    good = lint_text("AGENTS.md", GOOD).score
    bad = lint_text("AGENTS.md", "## no title\nwrite good code\n").score
    assert bad < good


def test_scaffold_python_passes_own_linter():
    content = render(project="Demo", stack="python")
    r = lint_text("AGENTS.md", content)
    assert r.ok
    assert r.score >= 80


def test_scaffold_node_passes_own_linter():
    content = render(project="Demo", stack="node")
    r = lint_text("AGENTS.md", content)
    assert r.ok


def test_cli_lint_pretty_returns_zero_for_good_file(tmp_path, capsys):
    f = tmp_path / "AGENTS.md"
    f.write_text(GOOD, encoding="utf-8")
    code = main(["lint", str(f)])
    out = capsys.readouterr().out
    assert code == 0
    assert "score" in out


def test_cli_lint_json_shape(tmp_path, capsys):
    f = tmp_path / "AGENTS.md"
    f.write_text(GOOD, encoding="utf-8")
    code = main(["lint", str(f), "--format", "json"])
    data = json.loads(capsys.readouterr().out)
    assert code == 0
    assert data["results"][0]["ok"] is True
    assert "score" in data["results"][0]


def test_cli_min_score_gate_fails(tmp_path):
    f = tmp_path / "AGENTS.md"
    f.write_text("## bad\nwrite good code\n", encoding="utf-8")
    code = main(["lint", str(f), "--min-score", "95"])
    assert code == 1


def test_cli_error_file_returns_one(tmp_path):
    f = tmp_path / "AGENTS.md"
    f.write_text("TODO: fill\n", encoding="utf-8")
    assert main(["lint", str(f)]) == 1


def test_cli_init_creates_passing_file(tmp_path, capsys):
    out = tmp_path / "AGENTS.md"
    code = main(["init", "--stack", "python", "--name", "Demo", "--output", str(out)])
    assert code == 0
    assert out.exists()
    r = lint_text(str(out), out.read_text(encoding="utf-8"))
    assert r.ok


def test_cli_init_refuses_overwrite(tmp_path):
    out = tmp_path / "AGENTS.md"
    out.write_text("# existing\n", encoding="utf-8")
    assert main(["init", "--output", str(out)]) == 1


def test_cli_rules_lists_rules(capsys):
    code = main(["rules"])
    out = capsys.readouterr().out
    assert code == 0
    assert "AM001" in out and "AM022" in out


def test_cli_discovers_files_in_directory(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "AGENTS.md").write_text(GOOD, encoding="utf-8")
    assert main(["lint", str(tmp_path)]) == 0
