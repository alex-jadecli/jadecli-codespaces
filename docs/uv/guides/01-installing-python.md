# Installing Python

Guide for installing Python versions with uv.

## Using uv to install Python

uv makes it easy to install and manage Python versions. You can install any Python version with a single command.

### Installing a specific version

```bash
uv python install 3.12
```

### Installing multiple versions

```bash
uv python install 3.11 3.12 3.13
```

### Using a specific Python version

Set the Python version in your `pyproject.toml`:

```toml
[project]
requires-python = ">=3.11"
```

Or specify it when creating a new project:

```bash
uv init --python 3.12
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/install-python/
