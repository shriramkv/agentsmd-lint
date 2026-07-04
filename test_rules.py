from agentsmd_lint import lint_text
from agentsmd_lint.rules import RuleConfig


def _ids(result):
    return {f.rule_id for f in result.findings}


def test_empty_file_is_error():
    r = lint_text("AGENTS.md", "")
    assert "AM001" in _ids(r)
    assert not r.ok


def test_missing_h1_warns():
    r = lint_text("AGENTS.md", "## Setup\n- run `pytest`\n")
    assert "AM002" in _ids(r)


def test_multiple_h1_warns():
    r = lint_text("AGENTS.md", "# One\n\n# Two\n")
    assert "AM002" in _ids(r)


def test_recommended_sections_absent_warns():
    r = lint_text("AGENTS.md", "# Title\n\nrandom notes here\n")
    assert "AM010" in _ids(r)


def test_recommended_sections_present_no_warn():
    text = "# Title\n\n## Testing\n- run `pytest -q`\n"
    r = lint_text("AGENTS.md", text)
    assert "AM010" not in _ids(r)


def test_commands_detected_in_code_block():
    text = "# T\n\n## Build\n```bash\npnpm build\n```\n"
    r = lint_text("AGENTS.md", text)
    assert "AM011" not in _ids(r)


def test_commands_detected_in_bullets():
    text = "# T\n\n## Test\n- run `pytest -q` before pushing\n"
    r = lint_text("AGENTS.md", text)
    assert "AM011" not in _ids(r)


def test_no_commands_warns():
    text = "# T\n\n## Overview\nA project that does things.\n"
    r = lint_text("AGENTS.md", text)
    assert "AM011" in _ids(r)


def test_vague_guidance_flagged():
    text = "# T\n\n## Style\n- write good code\n"
    r = lint_text("AGENTS.md", text)
    assert "AM020" in _ids(r)


def test_readme_echo_flagged():
    text = "# T\n\n## About\nThis project is a web framework.\n"
    r = lint_text("AGENTS.md", text)
    assert "AM021" in _ids(r)


def test_placeholder_content_is_error():
    text = "# T\n\n## Setup\nTODO: fill in\n"
    r = lint_text("AGENTS.md", text)
    assert "AM022" in _ids(r)
    assert not r.ok


def test_length_budget_warns_when_over():
    body = "word " * 1600
    text = f"# T\n\n## Testing\n- run `pytest`\n\n{body}"
    r = lint_text("AGENTS.md", text)
    assert "AM030" in _ids(r)


def test_section_length_info_when_long():
    cfg = RuleConfig(max_section_words=5)
    text = "# T\n\n## Big\nthis section has more than five words easily\n"
    r = lint_text("AGENTS.md", text, cfg)
    assert "AM031" in _ids(r)


def test_empty_section_warns():
    text = "# T\n\n## Setup\n\n## Testing\n- run `pytest`\n"
    r = lint_text("AGENTS.md", text)
    assert "AM040" in _ids(r)


def test_parent_section_with_subsections_not_empty():
    text = "# T\n\n## Group\n### Child\n- run `pytest`\n"
    r = lint_text("AGENTS.md", text)
    # 'Group' has a child section, so it should not be flagged empty.
    empties = [f for f in r.findings if f.rule_id == "AM040" and "Group" in f.message]
    assert not empties


def test_bare_url_info():
    text = "# T\n\n## Refs\nSee https://example.com for details\n"
    r = lint_text("AGENTS.md", text)
    assert "AM041" in _ids(r)


def test_disabled_rule_is_skipped():
    cfg = RuleConfig(disabled_rules={"AM020"})
    text = "# T\n\n## Style\n- write good code\n- run `pytest`\n"
    r = lint_text("AGENTS.md", text, cfg)
    assert "AM020" not in _ids(r)
