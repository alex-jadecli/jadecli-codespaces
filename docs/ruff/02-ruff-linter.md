# The Ruff Linter

Ruff's linting capabilities.

## What is linting?

Linting finds code issues like:
- Syntax errors
- Undefined variables
- Unused imports
- Code style violations
- Potential bugs

## Running the linter

Check your code:

```bash
ruff check .
```

Check specific file:

```bash
ruff check path/to/file.py
```

Fix issues automatically:

```bash
ruff check --fix .
```

## Linting rules

Ruff includes rules from:

- **E** - PEP 8 errors
- **F** - Pyflakes (undefined names, unused imports)
- **W** - PEP 8 warnings
- **I** - isort (import sorting)
- **UP** - pyupgrade (modernization)
- **B** - flake8-bugbear (bug detection)
- **C** - McCabe complexity
- **N** - pep8-naming
- **D** - pydocstyle (docstrings)
- **S** - bandit (security)
- And many more...

## Selecting rules

Enable specific rules:

```toml
[tool.ruff.lint]
select = [
    "E",    # PEP 8 errors
    "F",    # Pyflakes
    "W",    # PEP 8 warnings
    "I",    # isort
    "UP",   # pyupgrade
]
```

Ignore specific rules:

```toml
[tool.ruff.lint]
ignore = [
    "E501",  # Line too long
    "D100",  # Missing docstring
]
```

## Per-file ignores

Ignore rules for specific files:

```toml
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Unused imports
"test_*.py" = ["S101"]    # assert used
"docs/conf.py" = ["E501"] # Line too long
```

## Error codes

Common error codes:

| Code | Rule | Description |
|------|------|-------------|
| E501 | Line too long | Line exceeds max length |
| F401 | Unused import | Import not used |
| F841 | Unused variable | Variable assigned but unused |
| E302 | Expected 2 blank lines | Function spacing |
| W292 | No newline at end | Missing EOF newline |

## Preview rules

Enable experimental rules:

```toml
[tool.ruff.lint]
preview = true
```

## Rule groups

Rules are organized by category. Run to see available rules:

```bash
ruff rule --all
```

Show specific rule:

```bash
ruff rule E501
```

## Output formats

```bash
# Default format
ruff check .

# JSON format
ruff check --output-format json .

# Quiet mode
ruff check --quiet .

# Show statistics
ruff check --statistics .
```

## Watch mode

Monitor files for changes:

```bash
ruff check --watch .
```

## More Information

For complete details, visit: https://docs.astral.sh/ruff/linter/
