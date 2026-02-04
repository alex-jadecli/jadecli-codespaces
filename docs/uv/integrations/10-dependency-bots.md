# Dependency Bots Integration

Using uv with dependency update bots.

## What are dependency bots?

Dependency bots automatically check for updates and create pull requests to upgrade packages. Popular options include Dependabot, Renovate, and PyUp.

## Using with Dependabot

Configure `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    
    # Use uv.lock file
    allow:
      - dependency-type: "all"
    
    # Target Python version
    python:
      version: "3.12"
```

## Using with Renovate

Configure `renovate.json`:

```json
{
  "extends": ["config:base"],
  "python": {
    "version": "3.12"
  },
  "lockFileMaintenance": {
    "enabled": true
  }
}
```

## Using with PyUp

PyUp supports uv projects automatically. Just ensure your `pyproject.toml` follows standard Python packaging format.

## Benefits with uv

- **Lock file safety** - Dependabot respects `uv.lock`
- **Faster CI** - uv's speed reduces PR check times
- **Reliable updates** - Precise dependency resolution
- **Modern format** - Support for `pyproject.toml`

## Handling bot PRs

When bots update dependencies:

1. Review the dependency changes
2. Run tests locally: `uv sync && uv run pytest`
3. Update lock file: `uv lock`
4. Commit changes

## Combining with pre-commit

Use pre-commit hooks to validate bot PRs:

```yaml
repos:
  - repo: local
    hooks:
      - id: lock-check
        name: check lock file
        entry: bash -c "uv lock --check"
        language: system
        stages: [commit]
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/dependency-bots/
