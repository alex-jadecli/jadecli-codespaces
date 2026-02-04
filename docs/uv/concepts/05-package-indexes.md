# Package Indexes

Understanding package indexes in uv.

## What are package indexes?

Package indexes are repositories that host Python packages. By default, uv uses PyPI, but you can configure additional or alternative indexes.

## Default index

PyPI (https://pypi.org) is the default:

```bash
uv add requests
```

## Using alternative indexes

Configure in `pyproject.toml`:

```toml
[tool.uv.index]
default = "https://pypi.org/simple/"
```

Or with command line:

```bash
uv add requests --index-url https://custom-index.example.com
```

## Multiple indexes

Use multiple indexes with priority:

```toml
[tool.uv.index]
indexes = [
    { url = "https://private.example.com/simple", priority = "primary" },
    { url = "https://pypi.org/simple", priority = "supplemental" },
]
```

## Private indexes

For private indexes, use authentication:

```bash
uv add mypackage --index-url https://token@private.example.com/simple/
```

Or set credentials in environment variables:

```bash
export UV_INDEX_AUTH=token=mytoken
```

## Finding packages

uv searches all configured indexes in priority order to find packages and resolve dependencies.

## More Information

For complete details, visit: https://docs.astral.sh/uv/concepts/package-indexes/
