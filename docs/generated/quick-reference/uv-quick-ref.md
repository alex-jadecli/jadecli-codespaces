# UV Quick Reference

Fast Python package manager and project tool. **Drop-in replacement for pip + poetry + venv.**

## Installation & Setup

```bash
# Install uv (via curl)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

## Project Management

```bash
# Create new project
uv init my_project
cd my_project

# Create virtual environment (explicit)
uv venv

# Activate venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# List project dependencies
uv pip list
```

## Dependencies

```bash
# Add package (adds to pyproject.toml)
uv add requests
uv add --dev pytest      # Dev dependency
uv add --optional ml numpy scipy  # Optional group

# Update packages
uv lock --upgrade
uv sync                  # Sync venv from lock

# Remove package
uv remove requests

# Show dependency tree
uv pip tree
```

## Running Code

```bash
# Run script in project environment
uv run script.py arg1 arg2

# Run with Python version constraint
uv run --python 3.11 script.py

# Interactive Python
uv run python
```

## Tools (uvx)

```bash
# Run tool without project (uvx = isolated environment)
uvx ruff check .
uvx black script.py
uvx poetry --version

# Run with pinned version
uvx ruff==0.1.0 check .
```

## Configuration

```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-app"
version = "0.1.0"
description = ""
dependencies = [
    "requests>=2.31.0",
]

[dependency-groups]
dev = [
    "pytest>=7.0",
    "ruff",
]
```

## Publishing

```bash
# Build package
uv build

# Output: dist/my_app-0.1.0.tar.gz, dist/my_app-0.1.0-py3-whl

# Publish to PyPI (requires twine or uv plugin)
# (See docs for authentication setup)
```

## Troubleshooting

```bash
# Clear cache
uv cache prune

# Show cache info
uv cache info

# Check Python versions available
uv python list

# Install specific Python version
uv python install 3.12
```

## Python Version Management

```bash
# Use specific Python in project
uv python pin 3.11

# Override for single command
uv run --python 3.10 script.py

# Show active Python
uv python show
```

## Environment Variables

```bash
# UV_INDEX_URL - Custom PyPI index
# UV_CACHE_DIR - Custom cache location
# VIRTUAL_ENV - Active venv path
```

---

**Docs:** https://docs.astral.sh/uv/
