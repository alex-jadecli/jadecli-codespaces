# Running Scripts

Guide for running Python scripts with uv.

## Using uv run

The `uv run` command allows you to run Python scripts with automatic dependency management.

### Running a simple script

```bash
uv run script.py
```

### Running a script with dependencies

If your script needs dependencies, declare them in a comment:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import requests

response = requests.get("https://api.example.com")
print(response.json())
```

Then run it:

```bash
uv run script.py
```

### Installing dependencies for a script

```bash
uv run --with requests script.py
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/scripts/
