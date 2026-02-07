# Ty Quick Reference

Fast Python type checker. **Catch type errors before runtime with zero runtime overhead.**

## Installation

```bash
# Via uv (recommended)
uv add --dev ty

# Via pip
pip install ty

# Via uvx (run without project)
uvx ty
```

## Basic Commands

```bash
# Check types
ty check .
ty check path/to/file.py

# Show detailed diagnostics
ty check --show-diagnostics .

# Show specific file
ty check --only path/to/file.py

# Check with Python version target
ty check --python-version 3.10 .
```

## Type Annotations

```python
# Basic annotations
def greet(name: str) -> str:
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b

# Collections
from typing import List, Dict, Optional

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

# Optional (can be None)
def find_user(user_id: int) -> Optional[str]:
    return None if user_id < 0 else "user"

# Union types
from typing import Union

def parse(value: Union[str, int]) -> str:
    return str(value)
```

## Configuration (pyproject.toml)

```toml
[tool.ty]
python-version = "3.10"
strict = true              # Enforce strict checking
ignore-missing-imports = false

[[tool.ty.overrides]]
module = "legacy_library"
ignore-missing-imports = true
```

## Common Type Errors

```python
# ❌ Type mismatch
result = add("5", 10)  # Error: str instead of int

# ❌ Missing return
def process() -> str:
    return 42  # Error: int instead of str

# ❌ Undefined variable
def compute():
    return undefined_var  # Error: not defined

# ❌ Wrong argument count
def two_args(a: int, b: int) -> int:
    return a + b

result = two_args(5)  # Error: missing argument
```

## Type Checking Strategies

```python
# Type narrowing (if-checks)
def process(value: Union[str, int]) -> str:
    if isinstance(value, str):
        return value.upper()  # value is str
    else:
        return str(value)     # value is int

# Type assertions (when you know better)
from typing import cast

data: object = "hello"
text: str = cast(str, data)  # Tell type checker: trust me

# Generic types
from typing import TypeVar, Generic

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value
```

## IDE Integration

```bash
# VS Code settings.json
"[python]": {
    "editor.defaultFormatter": "ms-python.python"
},
"python.linting.enabled": true,
"python.linting.tyEnabled": true
```

## Ignoring Errors

```python
# Inline: ignore next line
x = some_function()  # type: ignore

# Inline: ignore specific error
result = bad_function()  # type: ignore[no-untyped-call]

# In docstring (for test functions)
"""
type: ignore[assignment]
"""
```

## Strict Mode

Enable in pyproject.toml:
```toml
[tool.ty]
strict = true
```

Enforces:
- All functions must have return type annotations
- All parameters must be annotated
- No implicit `Any` types
- Stricter None checking

## Common Type Definitions

```python
from typing import Any, Callable, Iterable, Sequence, Tuple

# Callable (function types)
callback: Callable[[int, str], bool]

# Sequence/Iterable
def process(items: Iterable[str]) -> None:
    for item in items:
        print(item)

# Tuple with specific types
pair: Tuple[str, int] = ("name", 42)

# Any (escape hatch)
data: Any = {"key": "value"}  # Type checker won't validate
```

## Workflow Example

```bash
# 1. Add type hints to code
# 2. Run type checker
ty check .

# 3. Fix type errors reported
# 4. Enable strict mode once errors clear
# 5. Commit types with code changes
```

---

**Docs:** https://docs.astral.sh/ty/
