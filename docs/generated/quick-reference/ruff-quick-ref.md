# Ruff Quick Reference

Extremely fast Python linter + formatter + import organizer. **Replaces pylint, flake8, black, isort.**

## Installation

```bash
# Via uv (recommended)
uv add --dev ruff

# Via pip
pip install ruff

# Via uvx (run without project)
uvx ruff
```

## Basic Commands

```bash
# Check code for issues
ruff check .
ruff check path/to/file.py

# Fix auto-fixable issues
ruff check --fix .
ruff check --fix --unsafe .  # Include unsafe fixes

# Format code (like Black)
ruff format .
ruff format path/to/file.py

# Check + format (common workflow)
ruff check --fix . && ruff format .
```

## Common Options

```bash
# Exclude directories
ruff check . --exclude venv,tests

# Select specific rules
ruff check . --select E,F      # Only pycodestyle, Pyflakes
ruff check . --ignore E501     # Ignore line too long

# Show rule codes
ruff check . --show-codes

# Output format
ruff check . --output-format json
ruff check . --output-format github
```

## Configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
# Enable rules
select = ["E", "F", "W", "I"]  # Errors, Pyflakes, Warnings, isort
ignore = ["E501"]  # Line too long

[tool.ruff.format]
# Formatter options
line-length = 100
indent-width = 4
```

## Rule Categories

| Code | Category | Purpose |
|------|----------|---------|
| E/W | pycodestyle | Style violations |
| F | Pyflakes | Logic errors, undefined names |
| I | isort | Import organization |
| N | pep8-naming | Naming conventions |
| D | pydocstyle | Docstring issues |
| C90 | mccabe | Complexity |
| UP | pyupgrade | Modern Python syntax |
| B | flake8-bugbear | Bug patterns |

## IDE Integration

```bash
# VS Code settings.json
"[python]": {
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "charliermarsh.ruff"
},
"ruff.showNotifications": "always"
```

## Workflow Example

```bash
# 1. Check and fix issues
ruff check --fix src/

# 2. Format code
ruff format src/

# 3. Verify no violations remain
ruff check src/
```

## Performance

- 10-100x faster than pylint, flake8, black
- Processes large codebases in seconds
- Minimal CPU/memory usage

## Ignore Violations

```python
# Inline: disable rule for line
x = 1  # noqa: E501

# Inline: disable rule for block
# noqa: F401
import unused_module

# Inline: disable all
result = potentially_unsafe()  # noqa
```

## Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [ --fix ]
      - id: ruff-format
```

---

**Docs:** https://docs.astral.sh/ruff/
