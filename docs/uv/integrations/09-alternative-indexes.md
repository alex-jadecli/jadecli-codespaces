# Alternative Package Indexes

Using uv with alternative or private package indexes.

## What are alternative indexes?

Alternative indexes allow you to use packages from sources other than PyPI, such as private company repositories or specialized package repositories.

## Configuring indexes

Configure in `pyproject.toml`:

```toml
[tool.uv.index]
default = { url = "https://pypi.org/simple/" }

[[tool.uv.index.indexes]]
name = "private"
url = "https://private.example.com/simple/"
priority = "primary"

[[tool.uv.index.indexes]]
name = "backup"
url = "https://backup.example.com/simple/"
priority = "supplemental"
```

## Using indexes with commands

Specify index when adding packages:

```bash
uv add mypackage --index-url https://private.example.com/simple/
```

## Index priorities

- **primary** - Searched first for all packages
- **supplemental** - Used if package not found in primary

## Authentication

Provide credentials for private indexes:

```bash
uv add mypackage --index-url https://token:password@private.example.com/simple/
```

Or via environment variables:

```bash
export UV_INDEX_AUTH=token
uv add mypackage --index-url https://private.example.com/simple/
```

## Trusted hosts

Allow insecure (HTTP) indexes:

```bash
uv add mypackage --index-url http://local-index:8080/simple/ --trusted-host local-index
```

## PyPI mirrors

Use PyPI mirrors for faster downloads:

```bash
uv add requests --index-url https://mirrors.aliyun.com/pypi/simple
```

## Artifactory and Nexus

Configure with enterprise repositories:

```toml
[[tool.uv.index.indexes]]
url = "https://artifactory.example.com/artifactory/api/pypi/pypi/simple"
priority = "primary"
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/integration-indexes/
