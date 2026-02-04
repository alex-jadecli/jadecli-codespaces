# Internals

Details about uv's internal architecture and design.

## Resolver internals

### Resolution algorithm

uv uses a two-phase resolution algorithm:

1. **Dependency discovery** - Fetch metadata for all versions
2. **Conflict resolution** - Find compatible version set

The resolver handles:
- Python version constraints
- Platform-specific dependencies
- Extras and optional dependencies
- Circular dependencies

### Performance optimizations

- **Parallel fetches** - Downloads metadata in parallel
- **Caching** - Caches metadata and wheels
- **Pruning** - Eliminates incompatible versions early
- **Backtracking** - Efficient dependency conflict resolution

### Version selection

By default, uv selects:
1. Latest compatible version
2. Respecting all constraints
3. Preferring wheels over source distributions
4. Supporting prerelease versions when needed

## Lock file format

The `uv.lock` file uses a custom text format:

```
version = 1
requires-python = ">=3.11"

[[package]]
name = "requests"
version = "2.31.0"
source = { type = "registry", url = "..." }
dependencies = [
    { name = "urllib3", version = "..." },
]
```

Format features:
- Human-readable
- Git-friendly (line-based)
- Deterministic (sorted output)
- Complete dependency tree

## Cache organization

Cache structure optimized for:
- **Fast lookups** - Index by package name
- **Efficient storage** - Deduplicated wheels
- **Expiration** - TTL-based invalidation
- **Integrity** - Hash verification

## Virtual environment layout

Standard `.venv/` structure:

```
.venv/
├── pyvenv.cfg          # Configuration
├── bin/ (Unix)         # Executables and scripts
│   ├── python
│   ├── pip
│   └── <tools>
├── Scripts/ (Windows)  # Executables
├── lib/                # Python packages
└── include/            # C headers
```

## Build system

uv uses a custom PEP 517 build backend:

- Handles pure Python projects efficiently
- Supports compiled extensions
- Respects `pyproject.toml` configuration
- Produces standard wheels and SDists

## Dependency graph

Internal representation:

- Directed acyclic graph (DAG)
- Nodes are packages/versions
- Edges represent dependencies
- Used for conflict detection

## Parallel execution

uv parallelizes:
- Package downloads
- Metadata fetches
- Wheel extraction
- Dependency resolution

Controlled by:
- System CPU count
- Job pool size
- I/O limits

## Platform-specific logic

Handles platform differences:

- **Markers** - PEP 508 environment markers
- **Wheels** - Platform-specific wheel selection
- **Python** - Version-specific code paths
- **Compatibility** - ABI and API changes

## Standard compliance

uv adheres to:
- **PEP 517** - Build system interface
- **PEP 518** - Build requirements
- **PEP 508** - Dependency specifiers
- **PEP 440** - Version identification
- **PEP 503** - Simple repository API

## Error handling

Robust error management:

- Network retry logic
- Partial download recovery
- Graceful degradation
- Informative error messages

## Memory efficiency

Optimizations:
- Streaming downloads
- Lazy evaluation
- Garbage collection tuning
- Efficient data structures

## More Information

For complete details, visit: https://docs.astral.sh/uv/reference/internals/
