# Python Versions

Managing Python versions with uv.

## What are Python versions?

uv can download, install, and manage multiple Python versions without system dependencies.

## Listing available versions

See which Python versions are available:

```bash
uv python list
```

## Installing Python versions

Install specific Python versions:

```bash
uv python install 3.12
uv python install 3.11 3.12 3.13
```

## Using a specific version

Specify the version in your project:

```toml
[project]
requires-python = ">=3.11,<4"
```

Or at runtime:

```bash
uv run --python 3.12 script.py
```

## Finding Python

uv will use:

1. The specified `requires-python` version
2. Environment variable `UV_PYTHON`
3. The default Python version
4. The first available Python version

## Python discovery

uv searches for Python in:

- System `PATH`
- pyenv installations
- Conda environments
- uv-managed installations

## Removing Python versions

```bash
uv python uninstall 3.11
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/concepts/python-versions/
