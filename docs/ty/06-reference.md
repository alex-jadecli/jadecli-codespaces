# Ty Reference

Complete reference for Ty type checker.

## CLI Commands

### ty check
Check types in project:

```bash
ty check [OPTIONS] [PATH]
```

Options:
- `--show-diagnostics` - Show all diagnostics
- `--verbose` - Verbose output
- `--python-version <VERSION>` - Override Python version
- `--strict` - Enable strict mode

### ty rules
List type checking rules:

```bash
ty rules [OPTIONS]
```

Options:
- `--detail` - Show detailed info
- `--all` - Show all rules

### ty version
Show version:

```bash
ty --version
```

### ty help
Show help:

```bash
ty --help
ty <command> --help
```

## Configuration options

### Python version
```toml
[tool.ty]
python-version = "3.10"
```

### Strict mode
```toml
[tool.ty]
strict = true
```

### File exclusions
```toml
[tool.ty]
exclude = ["tests/", ".venv/"]
```

## Exit codes

- `0` - No errors
- `1` - Type errors found
- `2` - Configuration error
- `3` - Internal error

## Environment variables

### TY_PYTHON_VERSION
Set target Python version:
```bash
export TY_PYTHON_VERSION=3.10
```

### TY_STRICT
Enable strict mode:
```bash
export TY_STRICT=1
```

### TY_VERBOSE
Enable verbose output:
```bash
export TY_VERBOSE=1
```

## Editor settings

### VS Code
```json
{
    "ty.enable": true,
    "ty.checkOnSave": true,
    "ty.pythonVersion": "3.10"
}
```

### PyCharm
Settings → Tools → Python → Type Checker

## Type annotations

### Basic types
```python
name: str
age: int
height: float
active: bool
```

### Containers
```python
from typing import List, Dict, Set, Tuple

items: List[int]
mapping: Dict[str, int]
tags: Set[str]
pair: Tuple[int, str]
```

### Optional and Union
```python
from typing import Optional, Union

value: Optional[int]
result: Union[int, str]
```

### Callable
```python
from typing import Callable

callback: Callable[[int, int], int]
```

### Generic
```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Box(Generic[T]):
    def get(self) -> T:
        ...
```

## Type checking patterns

### Type narrowing
```python
from typing import Union

def process(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return str(value)
    return value
```

### Type guards
```python
from typing import TypeGuard

def is_string(value: object) -> TypeGuard[str]:
    return isinstance(value, str)
```

### Protocol
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        ...
```

## Suppression

### Ignore file
```python
# ty: ignore_file
```

### Ignore line
```python
value = function()  # ty: ignore
```

### Ignore specific error
```python
value: str = 42  # ty: ignore[assignment]
```

## Useful links

- **Official docs**: https://docs.astral.sh/ty/
- **GitHub repo**: https://github.com/astral-sh/ty
- **Issue tracker**: https://github.com/astral-sh/ty/issues

## More Information

For complete details, visit: https://docs.astral.sh/ty/reference/
