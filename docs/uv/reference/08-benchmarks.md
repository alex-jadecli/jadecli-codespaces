# Benchmarks

Performance benchmarks and comparisons for uv.

## Dependency resolution

### Speed comparison

Typical project with 50+ dependencies:

- **uv** - ~2-5 seconds
- **pip** - ~30-60 seconds
- **Poetry** - ~15-30 seconds
- **PDM** - ~10-20 seconds

Speed improvement: **10-30x faster** than pip

### Large dependency tree

Complex project with 200+ transitive dependencies:

- **uv** - ~5-10 seconds
- **pip** - ~2-5 minutes
- **Poetry** - ~1-2 minutes

## Dependency locking

### Lock file generation

Creating a lock file for new project:

- **uv** - ~3-5 seconds
- **pip-tools** - ~20-40 seconds
- **Poetry** - ~15-30 seconds

### Lock file updates

Updating lock file with new dependency:

- **uv** - ~2-3 seconds
- **Poetry** - ~10-20 seconds

## Installation

### Virtual environment setup

Installing 50 dependencies:

- **uv** - ~5-10 seconds
- **pip** - ~15-30 seconds
- **Poetry** - ~20-40 seconds

### Cached installations

With warm cache:

- **uv** - ~1-2 seconds
- **pip** - ~5-10 seconds

## Parallel operations

uv's parallel downloads:

- Single dependency: ~2 seconds
- 10 parallel dependencies: ~2-3 seconds
- 50 parallel dependencies: ~4-5 seconds

**Speedup**: 10-15x for large dependency sets

## Memory usage

Peak memory during operations:

- **uv** - ~50-100 MB
- **pip** - ~200-400 MB
- **Poetry** - ~300-500 MB

**Reduction**: 3-5x less memory

## Cold start

Starting fresh with no cache:

- **uv** - ~3-5 seconds (resolve + download)
- **pip** - ~30-60 seconds
- **Poetry** - ~20-40 seconds

## Warm start

With local cache:

- **uv** - ~0.5-1 second
- **pip** - ~2-5 seconds

## Network efficiency

Bandwidth usage for resolving dependencies:

- **uv** - Minimal (optimized requests)
- **pip** - Standard (more requests)
- **Poetry** - Heavy (metadata caching)

## Consistency

Lock file consistency:

- **uv** - 100% reproducible
- **pip-tools** - Generally reliable
- **Poetry** - Generally reliable

## Real-world projects

Performance on actual projects:

### Django project (50 deps)
- **uv**: 3 seconds
- **pip**: 45 seconds

### Data Science (200+ deps)
- **uv**: 8 seconds
- **pip**: 120 seconds

### FastAPI microservice (30 deps)
- **uv**: 2 seconds
- **pip**: 25 seconds

## Factors affecting performance

- Number of dependencies
- Network speed
- Disk speed
- CPU count
- Cache state
- Python version availability

## Benchmarking methodology

All benchmarks use:
- Clean environment
- Warm cache (unless noted)
- Standard hardware
- Representative projects
- Multiple runs (average)

## Continuous improvement

uv is continuously optimized:
- Regular profiling
- Performance regressions testing
- Community feedback
- Latest Rust optimizations

## More Information

For complete details, visit: https://docs.astral.sh/uv/reference/benchmarks/
