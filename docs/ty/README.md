# Ty - Type Checker

Type checking for Python with Ty.

## What is Ty?

Ty is a Python type checker that helps you write safer, more reliable code by catching type errors before runtime.

## Key features

- **Static analysis** - Check types without running code
- **Fast** - Blazing fast type checking
- **Flexible** - Works with various Python versions
- **Standards compliant** - Follows PEP standards
- **Integrations** - Works with your favorite tools

## Installation

Install with uv:

```bash
uv add --dev ty
```

Or globally:

```bash
uvx ty
```

## Quick start

Check your code:

```bash
ty check .
```

Get detailed diagnostics:

```bash
ty check --show-diagnostics .
```

## Type checking

### Type annotations

Add type hints to your code:

```python
def greet(name: str) -> str:
    """Greet a person."""
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

### Type errors

Ty catches type mismatches:

```python
# Error: str received instead of int
result = add("5", 10)

# Error: int returned instead of str
def process() -> str:
    return 42
```

## Python version support

Configure target Python version:

```toml
[tool.ty]
python-version = "3.10"
```

## Documentation structure

- [Installation](./01-installation.md) - Getting started
- [Type checking](./02-type-checking.md) - How type checking works
- [Editor integration](./03-editor-integration.md) - IDE support
- [Configuration](./04-configuration.md) - Setup and customization
- [Rules](./05-rules.md) - Type checking rules
- [Reference](./06-reference.md) - Complete reference

## More Information

For complete details, visit: https://docs.astral.sh/ty/
