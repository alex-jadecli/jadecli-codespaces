# Using Tools

Guide for using tools with uv.

## Installing and running tools with uvx

The `uvx` command (uv execute) allows you to install and run tools from PyPI without creating a virtual environment.

### Running a tool

```bash
uvx <tool-name>
```

### Running a tool with a specific version

```bash
uvx <tool-name>==1.0.0
```

### Common examples

Install and run ruff (Python linter):

```bash
uvx ruff check .
```

Install and run black (Python formatter):

```bash
uvx black .
```

Install and run pipenv:

```bash
uvx pipenv shell
```

## Installing a tool

You can also install a tool for regular use:

```bash
uv tool install <tool-name>
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/tools/
