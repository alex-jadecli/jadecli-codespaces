# Reference

Complete reference documentation for uv.

## CLI Reference

- [Commands](./01-commands.md) - Complete command reference
  - Project management (init, sync, lock)
  - Dependency management (add, remove)
  - Code execution (run)
  - Tools (tool install, uvx)
  - Python management (python)
  - Building (build)
  - Others (pip, cache, version)

## Configuration

- [Settings](./02-settings.md) - Configuration schema
  - pyproject.toml settings
  - uv.toml configuration
  - Environment variable overrides
  - Command-line options
  - Configuration precedence

## Environment

- [Environment Variables](./03-environment-variables.md) - Variable reference
  - Index configuration
  - Python configuration
  - Cache configuration
  - Network configuration
  - Resolution configuration
  - Build configuration

## Storage and Installation

- [Storage](./04-storage.md) - Where uv stores data
  - Cache directory structure
  - Virtual environment layout
  - Tool directory
  - Python installations
  - Configuration file locations

- [Installer Options](./05-installer-options.md) - Installation customization
  - Installation methods
  - Environment variables
  - Shell configuration
  - Self-update
  - Package managers
  - Uninstallation

## Troubleshooting

- [Troubleshooting](./06-troubleshooting.md) - Common issues and solutions
  - Installation issues
  - Python-related issues
  - Dependency resolution issues
  - Performance issues
  - Authentication issues
  - Cache issues
  - Virtual environment issues
  - File permission issues
  - Networking issues

## Technical Details

- [Internals](./07-internals.md) - Architecture and design
  - Resolver internals
  - Lock file format
  - Cache organization
  - Virtual environment layout
  - Build system
  - Dependency graph
  - Parallel execution
  - Platform-specific logic
  - Standards compliance

- [Benchmarks](./08-benchmarks.md) - Performance metrics
  - Dependency resolution speed
  - Lock file generation
  - Installation performance
  - Memory usage
  - Real-world project performance

- [Policies](./09-policies.md) - Support and compatibility
  - Version numbering
  - Backward compatibility
  - Python version support
  - Platform support
  - License information
  - Security policy
  - Release cycle
  - Deprecation policy

## Quick reference

### Most common commands

```bash
uv init                    # Start new project
uv add <package>          # Add dependency
uv sync                   # Install dependencies
uv lock                   # Update lock file
uv run <script>           # Run script with dependencies
uv pip install <package>  # pip-compatible install
```

### Common settings

```bash
# pyproject.toml
requires-python = ">=3.11"
dependencies = ["requests", "click"]

# Environment
export UV_INDEX_URL=https://pypi.org/simple/
export UV_PYTHON=3.12
export UV_NO_NETWORK=1
```

## Organization tips

When working with uv:

1. **Always commit** `pyproject.toml` and `uv.lock`
2. **Ignore** `.venv/` in `.gitignore`
3. **Use dev dependencies** for tools and test frameworks
4. **Lock regularly** before commits
5. **Run tests** before releasing

## Common workflows

### Setting up a new project

```bash
uv init my-project
cd my-project
uv add requests numpy
uv sync
uv run python main.py
```

### Installing from requirements.txt

```bash
uv init --no-readme
uv pip compile requirements.txt
uv sync
```

### Publishing a package

```bash
uv build
uvx twine upload dist/*
```

## Useful links

- **Official docs**: https://docs.astral.sh/uv/
- **GitHub repo**: https://github.com/astral-sh/uv
- **Issue tracker**: https://github.com/astral-sh/uv/issues
- **Discussions**: https://github.com/astral-sh/uv/discussions

## More Information

For the complete documentation, visit: https://docs.astral.sh/uv/reference/
