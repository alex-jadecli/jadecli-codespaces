# Working on Projects

Guide for working on Python projects with uv.

## Creating a new project

Initialize a new project:

```bash
uv init my-project
cd my-project
```

## Adding dependencies

Add a package to your project:

```bash
uv add requests
```

Add a development dependency:

```bash
uv add --dev pytest
```

## Project structure

A typical uv project has this structure:

```
my-project/
├── pyproject.toml
├── README.md
├── src/
│   └── my_package/
│       └── __init__.py
└── tests/
    └── test_*.py
```

## Running your project

Install dependencies and run your project:

```bash
uv sync
uv run my-script.py
```

## Using the virtual environment

Activate the virtual environment:

```bash
source .venv/bin/activate
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/projects/
