# Troubleshooting

Solutions for common uv issues.

## Installation issues

### uv: command not found

**Cause**: uv is not in your PATH

**Solution**:
```bash
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Permission denied

**Cause**: uv binary lacks execute permissions

**Solution**:
```bash
chmod +x ~/.local/bin/uv ~/.local/bin/uvx
```

### Installation script fails

**Cause**: Missing curl or network issues

**Solution**:
```bash
# Try with wget instead
wget -qO- https://astral.sh/uv/install.sh | sh

# Or verify the script first
curl -LsSf https://astral.sh/uv/install.sh | less
```

## Python-related issues

### No Python found

**Cause**: Python not installed or not in PATH

**Solution**:
```bash
# Install Python with uv
uv python install 3.12

# Or specify Python path
export UV_PYTHON=/usr/bin/python3.12

# Or download a managed Python
uv python list
```

### Wrong Python version used

**Cause**: Multiple Python versions, wrong one selected

**Solution**:
```bash
# Check which Python is used
uv python find

# Specify version
uv run --python 3.12 script.py

# Or set in pyproject.toml
# requires-python = ">=3.12"
```

### uv python install fails

**Cause**: Unsupported platform or network issues

**Solution**:
```bash
# List supported versions
uv python list

# Try manual mode
export UV_PYTHON_DOWNLOADS=manual
uv python install 3.12

# Use system Python
export UV_PYTHON=/usr/bin/python3
```

## Dependency resolution issues

### No compatible version found

**Cause**: Dependency constraints conflict

**Solution**:
```bash
# Check current constraints
cat pyproject.toml

# Try relaxing version constraints
uv add requests>=2.28.0,<4.0

# View resolution details
uv add --verbose package_name
```

### Dependency locked to old version

**Cause**: Lock file needs updating

**Solution**:
```bash
# Update lock file
uv lock

# Or update specific package
uv lock --upgrade-package requests

# Force full upgrade
uv lock --upgrade
```

### Pre-release not selected

**Cause**: Prerelease preference disabled

**Solution**:
```bash
# Allow prereleases
export UV_PRERELEASE=allow

# Or update to prerelease
uv add "package>=1.0.0rc1"
```

## Performance issues

### Slow dependency resolution

**Cause**: Many dependencies or complex constraints

**Solution**:
```bash
# Use verbose mode to see progress
uv lock --verbose

# Check index response time
curl https://pypi.org/simple/requests/

# Try alternative index
uv add --index-url https://mirrors.aliyun.com/pypi/simple requests
```

### Slow package downloads

**Cause**: Network issues or large wheels

**Solution**:
```bash
# Clear cache and retry
uv cache clean

# Use parallel downloads (default)
uv sync

# Check internet connection
curl https://pypi.org/simple/
```

## Authentication issues

### 401 Unauthorized

**Cause**: Missing or invalid credentials

**Solution**:
```bash
# Set authentication token
export UV_INDEX_AUTH=your-token

# Or with URL
uv add --index-url https://token@private.example.com/simple/ package

# Or environment credentials
export UV_INDEX_USERNAME=myuser
export UV_INDEX_PASSWORD=mypass
```

### Certificate verification failed

**Cause**: SSL/TLS certificate issues

**Solution**:
```bash
# Trust host (use with caution)
uv add --trusted-host private.example.com \
       --index-url https://private.example.com/simple/ package

# Or disable SSL verification (NOT RECOMMENDED)
export UV_TLS_INSECURE=1
```

## Cache issues

### Stale cache

**Cause**: Outdated cached packages

**Solution**:
```bash
# Clear cache
uv cache clean

# Or clean specific package
uv cache clean requests

# Remove unused items
uv cache prune
```

### Cache permission denied

**Cause**: Cache directory permissions

**Solution**:
```bash
# Use custom cache directory
export UV_CACHE_DIR=/tmp/uv-cache
mkdir -p /tmp/uv-cache

# Or fix permissions
chmod -R u+w ~/.cache/uv/
```

## Virtual environment issues

### .venv not found

**Cause**: Virtual environment not created

**Solution**:
```bash
# Create virtual environment
uv sync

# Or manually create
python -m venv .venv
uv sync
```

### Stale virtual environment

**Cause**: Dependency changes not reflected

**Solution**:
```bash
# Rebuild virtual environment
rm -rf .venv
uv sync

# Or update only
uv sync --upgrade
```

## File permission issues

### Cannot create lock file

**Cause**: Directory permissions

**Solution**:
```bash
# Check directory
ls -la .

# Fix permissions
chmod u+w .

# Or recreate project in writable location
cd /tmp
uv init myproject
```

## Networking issues

### Network timeout

**Cause**: Slow network or unresponsive index

**Solution**:
```bash
# Increase timeout
export UV_HTTP_TIMEOUT=60

# Use offline mode with cache
export UV_NO_NETWORK=1
uv sync
```

### Cannot reach index

**Cause**: Network blocked or index down

**Solution**:
```bash
# Check connectivity
curl https://pypi.org/simple/

# Use offline mode
export UV_NO_NETWORK=1

# Switch to alternative index
export UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple
```

## Getting help

### View command help

```bash
uv --help
uv <command> --help
```

### Enable debug output

```bash
uv --verbose <command>
uv -vv <command>  # Extra verbose
```

### Check version

```bash
uv --version
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/reference/troubleshooting/
