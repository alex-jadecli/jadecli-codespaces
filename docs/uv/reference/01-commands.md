# Commands

Complete reference for uv commands.

## Project management

### uv init
Initialize a new uv project.

```bash
uv init [OPTIONS] [PATH]
```

Options:
- `--python <VERSION>` - Python version for the project
- `--no-readme` - Don't create README.md
- `--name <NAME>` - Project name

Example:
```bash
uv init my-project --python 3.12
```

### uv sync
Install dependencies from pyproject.toml into .venv.

```bash
uv sync [OPTIONS]
```

Options:
- `--frozen` - Require lock file to exist
- `--no-dev` - Skip development dependencies
- `--no-pre` - Don't build source distributions

Example:
```bash
uv sync --frozen
```

### uv lock
Generate or update uv.lock file.

```bash
uv lock [OPTIONS]
```

Options:
- `--upgrade` - Update all dependencies
- `--upgrade-package <PACKAGE>` - Update specific package
- `--check` - Verify lock file is up to date

Example:
```bash
uv lock --upgrade
```

## Dependency management

### uv add
Add a dependency to the project.

```bash
uv add [OPTIONS] <PACKAGES>...
```

Options:
- `--dev` - Add as development dependency
- `--optional <GROUP>` - Add to optional group
- `--index-url <URL>` - Use custom package index
- `--no-sync` - Don't sync after adding

Example:
```bash
uv add requests
uv add --dev pytest
```

### uv remove
Remove a dependency from the project.

```bash
uv remove [OPTIONS] <PACKAGES>...
```

Example:
```bash
uv remove requests
```

## Running code

### uv run
Run a script or command with dependencies.

```bash
uv run [OPTIONS] <COMMAND>
```

Options:
- `--python <VERSION>` - Use specific Python version
- `--with <PACKAGES>` - Add dependencies for this run

Example:
```bash
uv run python script.py
uv run --with requests pytest
```

## Tools

### uv tool install
Install a tool for global use.

```bash
uv tool install [OPTIONS] <PACKAGE>
```

Example:
```bash
uv tool install ruff
```

### uvx (uv execute)
Run a tool from PyPI without installation.

```bash
uvx [OPTIONS] <PACKAGE> [ARGS]...
```

Example:
```bash
uvx ruff check .
uvx pytest tests/
```

## Python management

### uv python
Manage Python versions.

```bash
uv python [SUBCOMMAND]
```

Subcommands:
- `list` - Show installed Python versions
- `install <VERSION>` - Install Python version
- `uninstall <VERSION>` - Remove Python version
- `dir` - Show Python directory

Example:
```bash
uv python list
uv python install 3.12
```

## Building

### uv build
Build project distributions.

```bash
uv build [OPTIONS] [PATH]
```

Options:
- `--wheel` - Build only wheel
- `--sdist` - Build only source distribution

Example:
```bash
uv build
```

## Other commands

### uv pip
pip-compatible command interface.

```bash
uv pip [SUBCOMMAND]
```

Subcommands:
- `install <PACKAGES>` - Install packages
- `freeze` - Show installed packages
- `list` - List packages
- `compile` - Compile requirements

### uv cache
Manage cache.

```bash
uv cache [SUBCOMMAND]
```

Subcommands:
- `clean` - Clear cache
- `dir` - Show cache directory
- `prune` - Remove unused items

### uv version
Show version information.

```bash
uv version
```

### uv help
Show help for commands.

```bash
uv help [COMMAND]
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/reference/cli/
