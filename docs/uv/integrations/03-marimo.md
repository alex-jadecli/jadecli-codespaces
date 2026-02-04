# marimo Integration

Using uv with marimo notebooks.

## What is marimo?

marimo is a Python reactive notebook that's great for interactive computing and data exploration.

## Installing marimo

Install marimo with uv:

```bash
uv add marimo
```

## Creating a marimo notebook

Create a new notebook:

```bash
uv run marimo create notebook.py
```

## Running marimo

Start the marimo server:

```bash
uv run marimo run notebook.py
```

## Editing notebooks

Edit in the browser with hot reloading:

```bash
uv run marimo edit notebook.py
```

## Project setup

Structure your marimo project:

```
my-project/
├── pyproject.toml
├── notebooks/
│   ├── explore.py
│   └── analyze.py
└── src/
    └── mymodule.py
```

## Adding dependencies

Install packages for use in notebooks:

```bash
uv add numpy pandas plotly
```

## Using local modules

Import from your project:

```python
import sys
sys.path.insert(0, '../src')

from mymodule import process_data
```

## Exporting to HTML

Convert marimo notebooks to HTML:

```bash
uv run marimo export notebook.py --to html
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/integration-marimo/
