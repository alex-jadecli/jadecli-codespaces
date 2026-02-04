# Pre-commit Integration

Using uv with pre-commit hooks.

## What is pre-commit?

pre-commit is a framework for managing and maintaining multi-language pre-commit hooks.

## Installing pre-commit

Install with uv:

```bash
uv add --dev pre-commit
```

## Creating `.pre-commit-config.yaml`

Configure hooks using uv tools:

```yaml
repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: ruff check
        entry: uvx ruff check
        language: system
        types: [python]
        stages: [commit]

      - id: ruff-format
        name: ruff format
        entry: uvx ruff format
        language: system
        types: [python]
        stages: [commit]

      - id: mypy
        name: mypy
        entry: uvx mypy
        language: system
        types: [python]
        stages: [commit]

      - id: pytest
        name: pytest
        entry: uvx pytest
        language: system
        types: [python]
        stages: [commit]
```

## Installing hooks

Install the hooks:

```bash
uv run pre-commit install
```

## Running hooks manually

```bash
uv run pre-commit run --all-files
```

## Using with Poetry/pip repos

You can also use external pre-commit repositories:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.28
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Configuration tips

- Use `language: system` for uv-managed tools
- Set `stages: [commit]` for automatic pre-commit execution
- Exclude specific files with `exclude`
- Use multiple `args` for tool options

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/integration-pre-commit/
