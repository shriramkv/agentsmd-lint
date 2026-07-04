from agentsmd_lint.parser import iter_code_blocks, parse


def test_parses_headings_and_bodies():
    text = "# Title\n\nintro\n\n## Setup\n- run `pip install`\n"
    doc = parse("AGENTS.md", text)
    assert [s.title for s in doc.sections] == ["Title", "Setup"]
    assert doc.sections[0].level == 1
    assert doc.sections[1].level == 2
    assert "intro" in doc.sections[0].body_text


def test_frontmatter_is_detected_and_skipped():
    text = "---\nkey: value\n---\n# Title\nbody\n"
    doc = parse("AGENTS.md", text)
    assert doc.has_frontmatter is True
    assert doc.sections[0].title == "Title"


def test_headings_inside_code_fences_are_ignored():
    text = "# Title\n\n```\n# not a heading\n```\n## Real\n"
    doc = parse("AGENTS.md", text)
    titles = [s.title for s in doc.sections]
    assert titles == ["Title", "Real"]


def test_iter_code_blocks_returns_inner_lines():
    text = "# T\n\n```bash\npnpm test\n```\n"
    doc = parse("AGENTS.md", text)
    blocks = iter_code_blocks(doc.sections[0])
    assert blocks == [["pnpm test"]]


def test_word_count_ignores_blank_lines():
    text = "# T\n\none two three\n\n"
    doc = parse("AGENTS.md", text)
    assert doc.sections[0].word_count == 3
