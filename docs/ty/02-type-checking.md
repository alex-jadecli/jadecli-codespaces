# Type Checking

Understanding type checking with Ty.

## What is type checking?

Type checking validates that your code uses values correctly:

- Variables have consistent types
- Functions receive correct argument types
- Return types match expected values
- Operations are valid for types

## Type annotations

### Basic types

```python
name: str = "Alice"
age: int = 30
height: float = 5.8
active: bool = True
```

### Function annotations

```python
def greet(name: str) -> str:
    """Greet a person."""
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

### Optional types

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    """Find user by ID."""
    # Returns either a string or None
    return None
```

### Collections

```python
from typing import List, Dict, Set

names: List[str] = ["Alice", "Bob"]
scores: Dict[str, int] = {"Alice": 95, "Bob": 87}
tags: Set[str] = {"python", "typing"}
```

## Type errors

Ty catches these errors:

### Type mismatch

```python
name: str = "Alice"
age: int = name  # Error: str cannot be assigned to int
```

### Wrong argument type

```python
def add(a: int, b: int) -> int:
    return a + b

result = add("5", 10)  # Error: str instead of int
```

### Missing return

```python
def process() -> str:
    print("Processing")
    # Error: Missing return value
```

### Attribute error

```python
text: str = "hello"
text.upper_case()  # Error: str has no attribute 'upper_case'
```

## Type narrowing

Ty understands type narrowing:

```python
from typing import Union

def process(value: Union[int, str]) -> int:
    if isinstance(value, int):
        return value * 2
    else:
        # Type is narrowed to str here
        return len(value)
```

## Generics

Use generic types:

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
    
    def get(self) -> T:
        return self.value

box: Box[int] = Box(42)
value: int = box.get()
```

## Running type checks

### Check entire project

```bash
ty check .
```

### Check specific file

```bash
ty check path/to/file.py
```

### Verbose output

```bash
ty check --verbose .
```

### Show diagnostics

```bash
ty check --show-diagnostics .
```

## Exit codes

- `0` - No type errors
- `1` - Type errors found

## Configuration

### Enable strict mode

```toml
[tool.ty]
strict = true
```

### Python version

```toml
[tool.ty]
python-version = "3.10"
```

## Common patterns

### Optional handling

```python
from typing import Optional

def get_value(key: str) -> Optional[int]:
    # Can return int or None
    ...

result = get_value("count")
if result is not None:
    # Type narrowed to int
    print(result + 1)
```

### Union types

```python
from typing import Union

def process(value: Union[int, str, float]) -> str:
    if isinstance(value, int):
        return f"Integer: {value}"
    elif isinstance(value, str):
        return f"String: {value}"
    else:
        return f"Float: {value}"
```

### Type aliases

```python
UserId = int
Username = str

def get_user(user_id: UserId) -> Optional[Username]:
    ...
```

## More Information

For complete details, visit: https://docs.astral.sh/ty/type-checking/
