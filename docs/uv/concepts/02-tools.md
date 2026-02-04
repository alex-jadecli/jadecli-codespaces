# Tools

Understanding tools and tool environments in uv.

## What are tools?

Tools are executable Python packages that you want to run. Unlike dependencies, tools don't need to be part of your project environment.

## Running tools with uvx

The `uvx` command runs any tool from PyPI without installation:

```bash
uvx ruff check .
uvx black .
uvx pytest tests/
```

## Installing tools

For frequently used tools, install them globally:

```bash
uv tool install ruff
uv tool install black
```

Tools are installed in an isolated environment at `~/.local/bin`.

## Tool environments

Each tool gets its own isolated environment, preventing dependency conflicts between tools.

## Common tools

- **ruff** - Fast Python linter
- **black** - Code formatter
- **pytest** - Testing framework
- **mypy** - Static type checker
- **pdoc** - API documentation generator

## More Information

For complete details, visit: https://docs.astral.sh/uv/concepts/tools/
