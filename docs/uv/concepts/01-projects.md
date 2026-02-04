# Projects

Understanding uv projects and their structure.

## What is a uv project?

A uv project is a Python package or application managed by uv. It uses a `pyproject.toml` file to define project metadata, dependencies, and configuration.

## Project structure

A typical uv project looks like:

```
my-project/
├── pyproject.toml          # Project configuration
├── uv.lock                 # Locked dependencies (auto-generated)
├── README.md               # Project documentation
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── module.py
├── tests/
│   ├── __init__.py
│   └── test_module.py
└── .venv/                  # Virtual environment
```

## pyproject.toml

The `pyproject.toml` file defines your project:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.28.0",
    "click>=8.0",
]

[project.optional-dependencies]
dev = ["pytest", "black"]

[tool.uv]
```

## Virtual environments

uv automatically manages a `.venv` directory for your project. Activate it with:

```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/concepts/projects/
