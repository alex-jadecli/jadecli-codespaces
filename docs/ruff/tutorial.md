# Ruff Tutorial

Getting started with Ruff.

## Installation

Install Ruff in your project:

```bash
uv add --dev ruff
```

## Basic usage

### Check your code

Check code for issues:

```bash
ruff check .
```

This will output any linting issues found:

```
src/main.py:1:1: F401 `os` imported but unused
src/main.py:3:1: E302 expected 2 blank lines, found 1
```

### Format your code

Format your code automatically:

```bash
ruff format .
```

All files will be formatted to match the style guide.

### Fix issues

Auto-fix fixable issues:

```bash
ruff check --fix .
```

Some issues can't be auto-fixed and need manual changes.

## Your first project

### Create a new project

```bash
uv init my-project
cd my-project
uv add --dev ruff
```

### Create a Python file

Create `src/hello.py`:

```python
import os
import sys
from typing import List


def greet(names):
    '''Say hello to names'''
    for name in names:
        print(f'Hello, {name}!')


if __name__ == '__main__':
    greet(['Alice', 'Bob'])
```

### Check with Ruff

```bash
ruff check src/
```

Issues found:

- F401: Unused `os` import
- D100: Missing module docstring
- D103: Missing function docstring

### Fix issues

Fix automatically fixable issues:

```bash
ruff check --fix src/
ruff format src/
```

### Result

After fixes, your code looks like:

```python
"""Greeting module."""
from typing import List


def greet(names: List[str]) -> None:
    """Say hello to names."""
    for name in names:
        print(f"Hello, {name}!")


if __name__ == "__main__":
    greet(["Alice", "Bob"])
```

## Configuration

### Setup pyproject.toml

```toml
[project]
name = "my-project"
version = "0.1.0"

[tool.ruff]
line-length = 88
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
```

## Workflow

Typical development workflow:

1. **Write code** - Create or modify Python files
2. **Check** - Run `ruff check .`
3. **Format** - Run `ruff format .`
4. **Fix issues** - Address remaining issues
5. **Commit** - Add to version control

## Integration

### Pre-commit

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.28
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### GitHub Actions

Add to workflow:

```yaml
- name: Check with Ruff
  run: uv run ruff check .

- name: Format check
  run: uv run ruff format --check .
```

## Common tasks

### Check specific file

```bash
ruff check path/to/file.py
```

### Format with custom settings

```bash
ruff format --line-length 100 .
```

### See what would change

```bash
ruff format --diff .
```

### Verbose output

```bash
ruff check --verbose .
```

### Watch mode

```bash
ruff check --watch .
```

## Next steps

- [The Ruff Linter](./02-ruff-linter.md) - Learn linting in detail
- [The Ruff Formatter](./03-ruff-formatter.md) - Learn formatting
- [Configuring Ruff](./04-configuring-ruff.md) - Customize behavior
- [Rules](./rules.md) - Understand all available rules

## More Information

For complete details, visit: https://docs.astral.sh/ruff/
