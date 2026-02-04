# uv Concepts

Core concepts for understanding uv.

## Core Concepts

- [Projects](./01-projects.md) - Project structure and configuration
- [Tools](./02-tools.md) - Running and managing CLI tools
- [Python Versions](./03-python-versions.md) - Managing Python versions
- [Configuration Files](./04-configuration-files.md) - Understanding config files
- [Package Indexes](./05-package-indexes.md) - Working with package repositories
- [Resolution](./06-resolution.md) - Dependency resolution process
- [The uv Build Backend](./07-uv-build-backend.md) - Building Python packages
- [Authentication](./08-authentication.md) - Authenticating with private indexes
- [Caching](./09-caching.md) - How uv caches packages and metadata
- [The pip Interface](./10-pip-interface.md) - Using uv's pip-compatible commands

## Quick Start

1. **Initialize a project**: Create a new project with `uv init`
2. **Add dependencies**: Use `uv add` to add packages
3. **Run code**: Execute with `uv run`
4. **Lock dependencies**: Generate `uv.lock` with `uv lock`
5. **Share project**: Commit `pyproject.toml` and `uv.lock`

## Key Features

- **Fast** - Parallel dependency resolution
- **Modern** - Follows Python packaging standards
- **Flexible** - Works with projects and tools
- **Compatible** - Drop-in replacement for pip and other tools
- **Reliable** - Reproducible installs with lock files

## Official Documentation

For more information, visit: https://docs.astral.sh/uv/concepts/
