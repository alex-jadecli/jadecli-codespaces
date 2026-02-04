# The pip Interface

Understanding uv's pip interface.

## What is the pip interface?

uv provides a `uv pip` command that mimics pip's interface while offering better performance and features.

## Using uv pip

uv pip works like pip but faster:

```bash
uv pip install requests
uv pip install -r requirements.txt
uv pip list
```

## Installing packages

Install single package:

```bash
uv pip install requests
```

Install from requirements file:

```bash
uv pip install -r requirements.txt
```

Install multiple packages:

```bash
uv pip install requests click
```

## Uninstalling packages

```bash
uv pip uninstall requests
uv pip uninstall -r requirements.txt
```

## Listing packages

```bash
uv pip list
uv pip show requests
```

## Exporting requirements

Export installed packages:

```bash
uv pip freeze > requirements.txt
```

## Compiling requirements

Compile requirements with pinned versions:

```bash
uv pip compile requirements.in
```

## Performance

uv pip is significantly faster than pip:

- Parallel dependency resolution
- Better caching
- Optimized downloads
- Faster package installation

## Compatibility

uv pip maintains compatibility with pip while adding:

- Better error messages
- Faster resolution
- Modern features
- Better defaults

## More Information

For complete details, visit: https://docs.astral.sh/uv/concepts/pip/
