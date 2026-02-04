# Publishing Packages

Guide for publishing Python packages with uv.

## Building your package

To build your package for distribution:

```bash
uv build
```

This creates:
- A wheel file (`.whl`)
- A source distribution (`.tar.gz`)

## Setting up for PyPI

1. Create an account on [PyPI](https://pypi.org)
2. Set up API tokens for authentication
3. Configure your `pyproject.toml` with project metadata:

```toml
[project]
name = "my-package"
version = "0.1.0"
description = "My awesome package"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
```

## Publishing to PyPI

Using twine:

```bash
uvx twine upload dist/*
```

Or using uv's built-in publishing (if available):

```bash
uv publish
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/publish/
