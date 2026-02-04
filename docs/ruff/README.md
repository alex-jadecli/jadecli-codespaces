# Ruff Overview

Ruff is an extremely fast Python linter and code formatter, written in Rust.

## What is Ruff?

Ruff combines the functionality of multiple Python tools into one:

- **Linter** - Find and report code issues (replaces pylint, flake8, etc.)
- **Formatter** - Automatically format code (replaces black)
- **Organizer** - Sort and organize imports (replaces isort)

## Key features

- **Speed** - 10-100x faster than alternatives
- **Comprehensive** - Hundreds of rules from multiple linters
- **Modern** - Built with Rust for performance
- **Compatible** - Drop-in replacement for common tools
- **Configurable** - Fine-grained rule configuration

## Installation

Install with uv:

```bash
uv add --dev ruff
```

Or install globally:

```bash
uvx ruff
```

Or with pip:

```bash
pip install ruff
```

## Quick start

Check your code:

```bash
ruff check .
```

Format your code:

```bash
ruff format .
```

Check and fix issues:

```bash
ruff check --fix .
```

## Testimonials

Ruff is used by:
- Major Python projects
- Enterprise organizations
- Open source communities
- Data science teams

See why teams choose Ruff for code quality.

## What's inside?

- [The Ruff Linter](./linter.md) - Code quality analysis
- [The Ruff Formatter](./formatter.md) - Code formatting
- [Configuring Ruff](./configuration.md) - Setup and customization
- [Rules](./rules.md) - Complete rule reference
- [Settings](./settings.md) - Configuration schema
- [Integrations](./integrations.md) - IDE and tool integrations

## Philosophy

Ruff is designed to be:
- **Fast** - Instant feedback on code
- **Reliable** - Consistent results
- **Practical** - Sensible defaults
- **Flexible** - Customizable for any project

## Documentation

- [Tutorial](./tutorial.md) - Getting started guide
- [Editors](./editors.md) - IDE integration
- [FAQ](./faq.md) - Common questions
- [Contributing](./contributing.md) - How to contribute

## Official documentation

For more information, visit: https://docs.astral.sh/ruff/
