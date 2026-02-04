# Configuring Ruff

Setting up Ruff for your project.

## Configuration file

Store Ruff configuration in `pyproject.toml`:

```toml
[tool.ruff]
# General settings
line-length = 88
target-version = "py38"

[tool.ruff.lint]
# Linter settings
select = ["E", "F", "W", "I"]
ignore = ["E501"]

[tool.ruff.format]
# Formatter settings
quote-style = "double"
```

Or use `ruff.toml`:

```toml
[lint]
select = ["E", "F", "W"]
ignore = ["E501"]

[format]
line-length = 100
```

## General settings

### line-length
Maximum line length (default: 88):

```toml
[tool.ruff]
line-length = 100
```

### target-version
Python version to target:

```toml
[tool.ruff]
target-version = "py38"  # Options: py37, py38, py39, ..., py313
```

### include/exclude
Files to include/exclude:

```toml
[tool.ruff]
include = ["*.py", "*.pyi"]
exclude = [".git", "__pycache__", "migrations/"]
```

## Lint settings

### select
Enable specific rules:

```toml
[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # Pyflakes
    "W",    # pycodestyle warnings
    "I",    # isort
    "UP",   # pyupgrade
]
```

### ignore
Disable specific rules:

```toml
[tool.ruff.lint]
ignore = [
    "E501",  # Line too long
    "D100",  # Missing module docstring
]
```

### per-file-ignores
Ignore rules for specific files:

```toml
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]     # Unused imports
"test_*.py" = ["S101"]       # assert used
"**/__init__.pyi" = ["F401"] # Type stub files
```

### allowed-confusables
Allow confusable variable names:

```toml
[tool.ruff.lint]
allowed-confusables = ["ρ", "σ"]  # Greek letters
```

## Format settings

### quote-style
Quote style preference:

```toml
[tool.ruff.format]
quote-style = "double"  # or "single"
```

### indent-width
Indentation width:

```toml
[tool.ruff.format]
indent-width = 4
```

### skip-magic-trailing-comma
Don't use magic trailing comma:

```toml
[tool.ruff.format]
skip-magic-trailing-comma = false
```

### line-ending
Line ending style:

```toml
[tool.ruff.format]
line-ending = "auto"  # or "lf", "cr", "crlf"
```

## isort settings

Configure import sorting:

```toml
[tool.ruff.lint.isort]
# Force single imports per line
force-single-line = true

# Group by import type
force-sort-within-sections = false

# Skip specific files
skip-gitignore = true
```

## McCabe complexity

Check function complexity:

```toml
[tool.ruff.lint.mccabe]
max-complexity = 10
```

## pydocstyle

Configure docstring checking:

```toml
[tool.ruff.lint.pydocstyle]
convention = "google"  # or "numpy", "pep257"
```

## Environment variables

Override with environment variables:

```bash
export RUFF_LINE_LENGTH=100
export RUFF_TARGET_VERSION=py310
```

## CLI overrides

Override config from command line:

```bash
ruff check --select E,F .
ruff format --line-length 100 .
```

## Example configurations

### Minimal

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F"]
```

### Comprehensive

```toml
[tool.ruff]
line-length = 88
target-version = "py39"

[tool.ruff.lint]
select = [
    "E",    # Errors
    "F",    # Pyflakes
    "W",    # Warnings
    "I",    # isort
    "UP",   # pyupgrade
    "N",    # pep8-naming
]
ignore = ["E501"]
extend-ignore = ["D100"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"test_*.py" = ["S101"]

[tool.ruff.format]
quote-style = "double"
indent-width = 4
```

## More Information

For complete details, visit: https://docs.astral.sh/ruff/configuration/
