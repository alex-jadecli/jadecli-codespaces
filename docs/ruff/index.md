# Ruff - Complete Documentation

Comprehensive guide to Ruff, the Python linter and formatter.

## Overview

Ruff is an extremely fast Python linter and code formatter written in Rust. It combines the functionality of multiple Python tools into one unified tool.

### Key features

- **Linting** - Find code issues and style violations
- **Formatting** - Automatically format code
- **Import organization** - Sort and organize imports
- **Speed** - 10-100x faster than alternatives
- **Compatibility** - Drop-in replacement for Black, isort, flake8, and more

## Getting started

1. [Installation](./01-installing-ruff.md) - Install Ruff
2. [Tutorial](./tutorial.md) - Learn the basics
3. [Configuring Ruff](./04-configuring-ruff.md) - Setup for your project

## Main sections

### Core functionality
- [The Ruff Linter](./02-ruff-linter.md) - Linting and code analysis
- [The Ruff Formatter](./03-ruff-formatter.md) - Code formatting
- [Configuring Ruff](./04-configuring-ruff.md) - Configuration and customization

### References
- [Rules](./rules.md) - Complete list of linting rules
- [Settings](./settings.md) - Configuration schema reference

### Integration
- [Editors](./editors.md) - IDE and editor support
- [Integrations](./integrations.md) - CI/CD and tool integration

### Additional resources
- [FAQ](./faq.md) - Frequently asked questions
- [Contributing](./contributing.md) - How to contribute

## Quick reference

### Common commands

```bash
ruff check .              # Check code
ruff check --fix .        # Fix issues
ruff format .             # Format code
ruff format --check .     # Check formatting
ruff rule E501            # Show specific rule
```

### Configuration example

```toml
[tool.ruff]
line-length = 88
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
```

## Linting rules

Ruff includes hundreds of rules from:
- **E** - PEP 8 errors
- **F** - Pyflakes
- **W** - PEP 8 warnings
- **I** - isort
- **UP** - pyupgrade
- **B** - flake8-bugbear
- **C** - McCabe
- **N** - pep8-naming
- **D** - pydocstyle
- **S** - bandit (security)
- And many more...

## Performance

Ruff is significantly faster than alternatives:
- Checking 1000s of files in seconds
- Lower memory usage
- Parallel processing
- Minimal overhead

## Why use Ruff?

✓ **Fast** - Instant feedback
✓ **Comprehensive** - Multiple tools in one
✓ **Reliable** - Consistent results
✓ **Modern** - Built with Rust
✓ **Compatible** - Works with existing tools
✓ **Configurable** - Flexible customization

## Community

- GitHub: https://github.com/astral-sh/ruff
- Discussions: https://github.com/astral-sh/ruff/discussions
- Issues: https://github.com/astral-sh/ruff/issues

## Official documentation

For more information, visit: https://docs.astral.sh/ruff/
