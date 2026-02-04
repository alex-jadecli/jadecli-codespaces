# Settings

Configuration reference for uv.

## pyproject.toml settings

### [project]

Core project configuration:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Name", email = "email@example.com"}
]
dependencies = [
    "requests>=2.28.0",
]
```

### [project.optional-dependencies]

Optional dependency groups:

```toml
[project.optional-dependencies]
dev = ["pytest", "black", "mypy"]
docs = ["sphinx"]
```

### [build-system]

Build system configuration:

```toml
[build-system]
requires = ["uv"]
build-backend = "uv.build"
```

### [tool.uv]

uv-specific settings:

```toml
[tool.uv]
# Python version for building
python-version = "3.12"

# Download Python automatically
managed-python = true

# Cache directory
cache-dir = "/path/to/cache"

# Dev dependencies
dev-dependencies = ["pytest"]
```

### [tool.uv.index]

Package index configuration:

```toml
[tool.uv.index]
default = { url = "https://pypi.org/simple/" }

[[tool.uv.index.indexes]]
name = "private"
url = "https://private.example.com/simple/"
priority = "primary"
```

## uv.toml settings

Dedicated uv configuration file:

```toml
[tool.uv]
python-downloads = "automatic"
managed-python = true

# Global settings
index-strategy = "lowest-match"
resolution-strategy = "lowest-match"
```

## Environment variables

### UV_INDEX_URL
Default package index URL:
```bash
export UV_INDEX_URL=https://custom-index.example.com/simple/
```

### UV_PYTHON
Python interpreter to use:
```bash
export UV_PYTHON=/usr/bin/python3.12
```

### UV_PYTHON_DOWNLOADS
Control automatic Python downloads:
```bash
export UV_PYTHON_DOWNLOADS=never
```

### UV_CACHE_DIR
Custom cache directory:
```bash
export UV_CACHE_DIR=/path/to/cache
```

### UV_NO_NETWORK
Disable network access:
```bash
export UV_NO_NETWORK=1
```

## Command-line options

### Global options

Available with most commands:

- `--python <VERSION>` - Python version
- `--index-url <URL>` - Package index URL
- `--cache-dir <DIR>` - Cache directory
- `--offline` - Disable network access
- `--quiet` / `-q` - Suppress output
- `--verbose` / `-v` - Verbose output

## Configuration precedence

Settings are applied in this order (highest to lowest):

1. Command-line arguments
2. Environment variables
3. Local `.uv.toml`
4. Local `pyproject.toml`
5. Global `~/.config/uv/uv.toml`
6. Default values

## More Information

For complete details, visit: https://docs.astral.sh/uv/reference/settings/
