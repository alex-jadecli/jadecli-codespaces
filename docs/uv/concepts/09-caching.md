# Caching

Understanding caching in uv.

## What is caching?

uv caches downloaded packages and metadata to speed up subsequent operations and reduce network usage.

## Cache locations

By default, uv stores cache in:

- **macOS/Linux**: `~/.cache/uv/`
- **Windows**: `%LOCALAPPDATA%\uv\cache`

## Cache structure

```
~/.cache/uv/
├── http-cache/          # HTTP response cache
├── simple-api/          # PyPI simple API cache
└── git/                 # Git repository cache
```

## Viewing cache

See cache statistics:

```bash
uv cache dir
```

## Clearing cache

Remove cached data:

```bash
uv cache clean
```

Clear specific package cache:

```bash
uv cache clean requests
```

## Custom cache location

Set cache directory:

```bash
export UV_CACHE_DIR=/path/to/cache
```

Or in `pyproject.toml`:

```toml
[tool.uv]
cache-dir = "/path/to/cache"
```

## Offline mode

Work without network access using cached packages:

```bash
export UV_NO_NETWORK=1
uv sync
```

## Cache invalidation

Cache is automatically invalidated when:

- Package indexes change
- Dependencies change
- Python versions change

## More Information

For complete details, visit: https://docs.astral.sh/uv/concepts/caching/
