# Installing Ruff

Getting started with Ruff.

## Installation methods

### With uv (recommended)

Install as development dependency:

```bash
uv add --dev ruff
```

Or install globally:

```bash
uvx ruff
```

### With pip

```bash
pip install ruff
```

### With pipx

```bash
pipx install ruff
```

### With Homebrew

```bash
brew install ruff
```

### With Conda

```bash
conda install -c conda-forge ruff
```

## Verify installation

Check that Ruff is installed:

```bash
ruff --version
```

## Project setup

### Add to pyproject.toml

Configure Ruff in your project:

```toml
[tool.ruff]
line-length = 88
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "W"]
ignore = ["E501"]  # Ignore line too long

[tool.ruff.format]
quote-style = "double"
```

## First run

Check your code:

```bash
ruff check .
```

Format your code:

```bash
ruff format .
```

## Editor integration

### VS Code

Install the Ruff extension:

```bash
uvx code-server --install-extension charliermarsh.ruff
```

Or search for "Ruff" in the VS Code marketplace.

### PyCharm

1. Install the Ruff plugin from marketplace
2. Configure in Settings → Tools → Python → Ruff

### Vim/Neovim

Use with coc.nvim or vim-lsp:

```vim
" In your LSP config
Plug 'neoclide/coc.nvim'
" Configure ruff language server
```

## GitHub Actions

Use Ruff in CI:

```yaml
- name: Lint with Ruff
  run: ruff check .

- name: Format check
  run: ruff format --check .
```

## Pre-commit

Use with pre-commit hooks:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.28
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Next steps

- [Tutorial](./tutorial.md) - Learn the basics
- [Configuring Ruff](./configuration.md) - Customize behavior
- [Rules](./rules.md) - Understand available rules

## More Information

For complete details, visit: https://docs.astral.sh/ruff/installation/
