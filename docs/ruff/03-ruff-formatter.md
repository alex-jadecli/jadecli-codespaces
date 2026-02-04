# The Ruff Formatter

Ruff's code formatting capabilities.

## What is formatting?

Code formatting automatically adjusts:
- Indentation
- Spacing
- Line breaks
- Quote style
- Trailing commas

## Running the formatter

Format your code:

```bash
ruff format .
```

Format specific file:

```bash
ruff format path/to/file.py
```

Check without modifying:

```bash
ruff format --check .
```

## Formatter features

### Consistent style

- Automatic code style
- No configuration needed (opinionated)
- Matches Black's output
- Reproducible results

### Smart formatting

- Respects line length
- Handles complex expressions
- Maintains readability
- Preserves logical structure

### Import organization

- Sorts imports alphabetically
- Groups imports by type
- Removes unused imports
- Adds missing newlines

## Configuration

### Basic options

```toml
[tool.ruff.format]
# Line length (default: 88)
line-length = 88

# Quote style
quote-style = "double"  # or "single"

# Indentation
indent-width = 4

# Include/exclude
include = ["*.py"]
exclude = ["tests/"]
```

### Quote style

Choose quote preference:

```toml
[tool.ruff.format]
quote-style = "double"  # Prefer "double"
```

The formatter will normalize quotes while respecting your preference.

## Compatibility with Black

The Ruff formatter is designed to be compatible with Black:

- Same default line length (88)
- Same quote handling
- Same import organization
- Drop-in replacement

## Before and after

### Before

```python
import   os
import sys
from typing import Dict,List,Optional


def process( data   , verbose=False ):
    result={'status':'ok','count':0}
    if verbose: print('Processing')
    return result
```

### After

```python
import os
import sys
from typing import Dict, List, Optional


def process(data, verbose=False):
    result = {"status": "ok", "count": 0}
    if verbose:
        print("Processing")
    return result
```

## Excluding code

Disable formatting for specific code:

```python
# fmt: off
irregular_code = {'x':1,'y':2}  # Stay as is
# fmt: on
```

## CLI options

```bash
ruff format .              # Format files
ruff format --check .      # Check without changing
ruff format --diff .       # Show changes
ruff format --line-length 100 .  # Custom line length
```

## Performance

The Ruff formatter is extremely fast:

- Formats 1000s of files in seconds
- Lower memory usage than alternatives
- Parallel processing
- Minimal overhead

## Diff preview

See what will change:

```bash
ruff format --diff .
```

## More Information

For complete details, visit: https://docs.astral.sh/ruff/formatter/
