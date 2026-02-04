# Environment Variables

Complete reference for uv environment variables.

## Index configuration

### UV_INDEX_URL
Default package index URL.

```bash
export UV_INDEX_URL=https://pypi.org/simple/
```

### UV_INDEX_AUTH
Authentication token for indexes.

```bash
export UV_INDEX_AUTH=token
```

### UV_INDEX_USERNAME
Username for index authentication.

```bash
export UV_INDEX_USERNAME=myuser
```

### UV_INDEX_PASSWORD
Password for index authentication.

```bash
export UV_INDEX_PASSWORD=mypass
```

## Python configuration

### UV_PYTHON
Python interpreter path.

```bash
export UV_PYTHON=/usr/bin/python3.12
export UV_PYTHON=3.12  # Version number
export UV_PYTHON=pypy3.11  # PyPy
```

### UV_PYTHON_DOWNLOADS
Control automatic Python downloads.

```bash
export UV_PYTHON_DOWNLOADS=automatic  # Default
export UV_PYTHON_DOWNLOADS=manual     # Never auto-download
export UV_PYTHON_DOWNLOADS=never      # Disable downloads
```

### UV_PYTHON_PREFERENCE
Prefer certain Python implementations.

```bash
export UV_PYTHON_PREFERENCE=only-system  # System Python only
export UV_PYTHON_PREFERENCE=managed      # Managed Python first
```

## Cache configuration

### UV_CACHE_DIR
Custom cache directory.

```bash
export UV_CACHE_DIR=/path/to/cache
```

### UV_CACHE_DISABLED
Disable caching.

```bash
export UV_CACHE_DISABLED=1
```

## Network configuration

### UV_NO_NETWORK
Disable all network access (offline mode).

```bash
export UV_NO_NETWORK=1
```

### UV_HTTP_TIMEOUT
HTTP request timeout in seconds.

```bash
export UV_HTTP_TIMEOUT=30
```

### UV_INSECURE_HOSTS
Allow insecure HTTP hosts.

```bash
export UV_INSECURE_HOSTS=localhost,internal-host
```

## Resolution configuration

### UV_RESOLUTION_STRATEGY
Dependency resolution strategy.

```bash
export UV_RESOLUTION_STRATEGY=highest    # Latest versions
export UV_RESOLUTION_STRATEGY=lowest     # Lowest versions
```

### UV_PRERELEASE
Include prerelease versions.

```bash
export UV_PRERELEASE=allow  # Allow prereleases
export UV_PRERELEASE=if-necessary  # Only if needed
```

## Build configuration

### UV_BUILD_PYTHON
Python for building packages.

```bash
export UV_BUILD_PYTHON=3.12
```

### UV_NO_BUILD_ISOLATION
Disable build isolation.

```bash
export UV_NO_BUILD_ISOLATION=1
```

## Output configuration

### UV_QUIET
Suppress output.

```bash
export UV_QUIET=1
```

### UV_VERBOSE
Verbose output.

```bash
export UV_VERBOSE=1
```

### UV_NO_COLOR
Disable colored output.

```bash
export UV_NO_COLOR=1
```

## Path configuration

### UV_TOOL_DIR
Directory for installed tools.

```bash
export UV_TOOL_DIR=/path/to/tools
```

## Experimental features

### UV_EXPERIMENTAL_RESOLVER
Enable experimental resolver features.

```bash
export UV_EXPERIMENTAL_RESOLVER=1
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/reference/environment-variables/
