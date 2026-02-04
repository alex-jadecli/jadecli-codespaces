# Configuration

Configuring Ty for your project.

## Configuration file

Store configuration in `pyproject.toml`:

```toml
[tool.ty]
# Python version to target
python-version = "3.10"

# Enable strict mode
strict = false

# Show all diagnostics
show-all = false
```

Or create `ty.toml`:

```toml
[ty]
python-version = "3.10"
strict = true
```

## General settings

### python-version
Target Python version:

```toml
[tool.ty]
python-version = "3.10"  # 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
```

### strict
Enable strict type checking:

```toml
[tool.ty]
strict = true
```

In strict mode:
- All values must be typed
- No implicit `Any` types
- Stricter checking overall

## Checking options

### show-all
Show all diagnostics:

```toml
[tool.ty]
show-all = false  # Show only errors
```

### exclude
Exclude files/directories:

```toml
[tool.ty]
exclude = [
    "tests/",
    "migrations/",
    ".venv/",
]
```

### include
Include specific files:

```toml
[tool.ty]
include = ["src/", "lib/"]
```

## Module discovery

### module-paths
Add to module search path:

```toml
[tool.ty]
module-paths = ["src/", "lib/"]
```

## Python version

### min-version
Minimum supported Python version:

```toml
[tool.ty]
min-version = "3.8"
```

### max-version
Maximum supported Python version:

```toml
[tool.ty]
max-version = "3.13"
```

## File exclusions

### Exclude patterns

```toml
[tool.ty]
exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "build",
    "dist",
    ".pytest_cache",
    ".mypy_cache",
]
```

## Suppression

### Ignore files

Skip checking entire files:

```python
# ty: ignore_file
# This file is not type checked
```

### Ignore lines

Ignore specific lines:

```python
result = function_without_types()  # ty: ignore
```

### Ignore errors

Ignore specific errors:

```python
value: str = 42  # ty: ignore[assignment]
```

## Rules and diagnostics

### Diagnostic levels

```toml
[tool.ty]
# Default: show errors and warnings
# Can be: error, warning, note, disabled
```

### Suppress rules

Suppress specific diagnostic codes:

```toml
[tool.ty]
suppress = [
    "W001",  # Example warning
    "E002",  # Example error
]
```

## Type checking features

### Reveal type

Show inferred types:

```python
from ty import reveal_type

value = 42
reveal_type(value)  # int
```

### Type aliases

```python
UserId = int
Username = str

def get_user(uid: UserId) -> Optional[Username]:
    ...
```

### Type guards

```python
from typing import TypeGuard

def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)
```

## Environment variables

Override configuration:

```bash
export TY_PYTHON_VERSION=3.10
export TY_STRICT=1
export TY_EXCLUDE=tests,build
```

## CLI overrides

Override from command line:

```bash
ty check --python-version 3.10 .
ty check --strict .
```

## Example configurations

### Minimal

```toml
[tool.ty]
python-version = "3.10"
```

### Comprehensive

```toml
[tool.ty]
python-version = "3.10"
strict = true
show-all = false

exclude = [
    ".git",
    ".venv",
    "migrations/",
    "tests/",
]

suppress = [
    "W001",
]
```

## More Information

For complete details, visit: https://docs.astral.sh/ty/configuration/
