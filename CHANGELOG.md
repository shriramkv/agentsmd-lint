# Changelog

All notable changes to this project are documented here. This project follows
[semantic versioning](https://semver.org/).

## [0.1.0] - 2026-07-04

### Added
- Initial release.
- `lint`, `init`, and `rules` CLI commands.
- 11 built-in rules (AM001–AM041) covering structure, command presence,
  vagueness, README duplication, generated-content detection, and length.
- Transparent 0–100 quality score.
- Pretty and JSON reporters.
- TOML configuration via `pyproject.toml` or `.agentsmd-lint.toml`.
- Python and Node scaffold templates.
- GitHub Action and pre-commit hook.
