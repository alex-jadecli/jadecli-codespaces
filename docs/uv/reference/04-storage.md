# Storage

Information about where uv stores data on your system.

## Cache directory

uv stores cache in:

- **macOS/Linux**: `~/.cache/uv/` or `$XDG_CACHE_HOME/uv/`
- **Windows**: `%LOCALAPPDATA%\uv\cache`

View cache location:

```bash
uv cache dir
```

## Cache structure

```
~/.cache/uv/
├── http-cache/          # HTTP response cache
│   └── ...
├── simple-api/          # PyPI simple API responses
│   └── ...
├── wheels/              # Downloaded wheels
│   └── ...
├── sdist/               # Downloaded source distributions
│   └── ...
└── git/                 # Cloned git repositories
    └── ...
```

## Clearing cache

Remove all cache:

```bash
uv cache clean
```

Remove specific package cache:

```bash
uv cache clean requests
```

## Virtual environment directory

Projects store virtual environments in `.venv/`:

```
my-project/
├── pyproject.toml
├── uv.lock
└── .venv/              # Virtual environment
    ├── bin/            # Executables (macOS/Linux)
    ├── Scripts/        # Executables (Windows)
    ├── lib/            # Python packages
    └── pyvenv.cfg      # Config file
```

## Global tool directory

Tools are installed in:

- **macOS/Linux**: `~/.local/bin/`
- **Windows**: `%APPDATA%\uv\bin`

View tool directory:

```bash
uv tool dir
```

## Python installations directory

Downloaded Python versions stored in:

- **macOS/Linux**: `~/.local/share/uv/python/`
- **Windows**: `%APPDATA%\uv\python`

View Python directory:

```bash
uv python dir
```

## Lock file

The `uv.lock` file is stored in project root:

```
my-project/
├── pyproject.toml
├── uv.lock             # Lock file (commit to version control)
└── .venv/
```

## Configuration files

uv looks for config in:

1. Local `pyproject.toml` or `uv.toml`
2. `~/.config/uv/uv.toml` (user config, if exists)

## Storage reference

- **XDG_CACHE_HOME** - Override cache directory
- **XDG_CONFIG_HOME** - Override config directory (Linux)
- **HOME** - User home directory
- **LOCALAPPDATA** - Local app data (Windows)
- **APPDATA** - App data (Windows)

## Temporary files

Temporary files during operations are stored in system temp:

- **macOS/Linux**: `/tmp/`
- **Windows**: `%TEMP%\`

## Disk usage

Check cache size:

```bash
du -sh ~/.cache/uv/
```

Clean unused cache entries:

```bash
uv cache prune
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/reference/storage/
