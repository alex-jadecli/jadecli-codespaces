# Integrations

Guide for integrating uv with other tools and platforms.

## IDE Integration

### VS Code

Install the Python extension and configure it to use uv:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

### PyCharm

PyCharm automatically detects uv projects. Just point to the `.venv` directory as your interpreter.

## CI/CD Integration

### GitHub Actions

Use uv in your GitHub Actions workflow:

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v1

- name: Run tests
  run: uv run pytest
```

### GitLab CI

```yaml
test:
  image: python:3.12
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="/root/.local/bin:$PATH"
  script:
    - uv run pytest
```

## Docker Integration

Use uv in Docker:

```dockerfile
FROM ghcr.io/astral-sh/uv:latest

COPY pyproject.toml uv.lock /app/
WORKDIR /app

RUN uv sync

COPY . .
CMD ["uv", "run", "main.py"]
```

## Pre-commit Integration

Add uv tools to your pre-commit configuration:

```yaml
repos:
  - repo: local
    hooks:
      - id: ruff
        name: ruff
        entry: uvx ruff check
        language: system
        types: [python]
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/integrations/
