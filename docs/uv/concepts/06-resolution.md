# Resolution

Understanding dependency resolution in uv.

## What is resolution?

Resolution is the process of finding compatible versions of all dependencies and their transitive dependencies.

## How uv resolves dependencies

1. Read project dependencies from `pyproject.toml`
2. Query package indexes for available versions
3. Find a combination that satisfies all constraints
4. Lock the resolved versions in `uv.lock`

## Version constraints

Specify allowed versions:

```toml
dependencies = [
    "requests>=2.28.0",      # Minimum version
    "django<5.0",            # Maximum version
    "flask>=2.0,<3.0",       # Range
    "numpy==1.24.0",         # Exact version
    "pandas~=2.0",           # Compatible version
]
```

## Resolution algorithm

uv uses a fast, reliable resolution algorithm that:

- Handles complex dependency graphs efficiently
- Respects Python version constraints
- Resolves extras and optional dependencies
- Detects conflicts early

## Lock files

The `uv.lock` file stores the resolved dependencies:

```bash
uv lock
uv sync  # Install from lock file
```

## Updating dependencies

Update to latest compatible versions:

```bash
uv add --upgrade requests
uv lock --upgrade
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/concepts/resolution/
