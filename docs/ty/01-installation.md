# Installation

Getting started with Ty.

## Installation methods

### With uv (recommended)

Install as development dependency:

```bash
uv add --dev ty
```

Or install globally:

```bash
uvx ty
```

### With pip

```bash
pip install ty
```

### With pipx

```bash
pipx install ty
```

### With Homebrew

```bash
brew install ty
```

## Verify installation

Check that Ty is installed:

```bash
ty --version
```

## Project setup

### Add to pyproject.toml

Configure Ty in your project:

```toml
[tool.ty]
python-version = "3.10"
strict = true
```

## First run

Type check your code:

```bash
ty check .
```

Check with detailed output:

```bash
ty check --show-diagnostics .
```

## Editor integration

### VS Code

1. Install the Ty extension from marketplace
2. Configure in settings.json:

```json
{
    "ty.checkOnSave": true,
    "ty.showDiagnostics": true
}
```

### PyCharm

1. Install the Ty plugin
2. Configure in Settings → Tools → Python → Type Checker

### Vim/Neovim

Use with coc.nvim or vim-lsp:

```vim
" Configure Ty language server
```

## Pre-commit

Use with pre-commit:

```yaml
repos:
  - repo: local
    hooks:
      - id: ty
        name: ty type check
        entry: uvx ty check
        language: system
        types: [python]
```

## GitHub Actions

Use in CI:

```yaml
- name: Type check with Ty
  run: ty check .
```

## Configuration

### Basic options

```toml
[tool.ty]
# Python version
python-version = "3.10"

# Strict mode
strict = true

# Show all diagnostics
show-all = false
```

## Next steps

- [Type checking](./02-type-checking.md) - Learn type checking
- [Configuration](./04-configuration.md) - Customize Ty
- [Rules](./05-rules.md) - Understand rules

## More Information

For complete details, visit: https://docs.astral.sh/ty/installation/
