# Rules

Type checking rules and diagnostics.

## Diagnostic categories

### Errors (E)

Critical type errors that must be fixed:

| Code | Name | Description |
|------|------|-------------|
| E001 | Type mismatch | Value type doesn't match annotation |
| E002 | Missing return | Function missing required return |
| E003 | Undefined name | Variable or function not defined |
| E004 | Missing attribute | Type has no such attribute |
| E005 | Wrong argument type | Function argument has wrong type |
| E006 | Argument count | Wrong number of function arguments |

### Warnings (W)

Potential issues that should be reviewed:

| Code | Name | Description |
|------|------|-------------|
| W001 | Unused variable | Variable assigned but not used |
| W002 | Unused import | Import not used in module |
| W003 | Unreachable code | Code after return statement |
| W004 | Redundant cast | Unnecessary type cast |
| W005 | Implicit any | Type implicitly assumed to be `Any` |

## Type checking rules

### Type assignment

Strict checking of type assignments:

```python
# OK
x: int = 42

# Error: E001
x: int = "hello"
```

### Function returns

Check function return types:

```python
def process() -> str:
    return "hello"  # OK
    return 42       # Error: E002
```

### Function arguments

Check argument types:

```python
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)        # OK
add("1", "2")    # Error: E005
add(1)           # Error: E006
```

### Attribute access

Check attribute access:

```python
text: str = "hello"
text.upper()     # OK
text.upper_case()  # Error: E004
```

## Advanced rules

### Generic types

Checking generic type correctness:

```python
from typing import List

items: List[int] = [1, 2, 3]  # OK
items: List[int] = [1, "2", 3]  # Error: type mismatch
```

### Union types

Type narrowing with Union:

```python
from typing import Union

def process(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return str(value)  # OK
    return value           # OK (narrowed to str)
```

### Optional types

Handling Optional:

```python
from typing import Optional

def get_value() -> Optional[int]:
    return None

value = get_value()
print(value + 1)  # Error: int | None doesn't support +
if value is not None:
    print(value + 1)  # OK (narrowed to int)
```

## Suppression

### File suppression

Ignore entire file:

```python
# ty: ignore_file
```

### Line suppression

Ignore specific line:

```python
value: str = 42  # ty: ignore
```

### Code suppression

Ignore specific error code:

```python
value: str = 42  # ty: ignore[assignment]
```

## Strict mode rules

Enable strict checking:

```toml
[tool.ty]
strict = true
```

Strict mode enforces:
- All values must have explicit types
- No implicit `Any` types
- All function returns must be typed
- Strict null checking

## Python version specific

Rules may vary by Python version:

```toml
[tool.ty]
python-version = "3.10"  # Union X | Y syntax allowed
```

## Ignore patterns

### Ignore errors

```python
from typing import Any

unsafe: Any = get_value()  # Any disables type checking
```

### Type ignoring

```python
value = function_call()  # type: ignore
```

## View available rules

```bash
ty rules           # List all rules
ty rules --detail  # Show detailed info
```

## More Information

For complete details, visit: https://docs.astral.sh/ty/rules/
