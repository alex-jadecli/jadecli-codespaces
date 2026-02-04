# Jupyter Integration

Using uv with Jupyter notebooks.

## Installing Jupyter

Install Jupyter with uv:

```bash
uv add jupyter
```

## Running Jupyter

Start Jupyter notebook:

```bash
uv run jupyter notebook
```

Or Jupyter lab:

```bash
uv run jupyter lab
```

## Project structure

Organize your Jupyter project:

```
my-project/
├── pyproject.toml
├── notebooks/
│   ├── 01_exploration.ipynb
│   └── 02_analysis.ipynb
└── src/
    └── mymodule.py
```

## Adding dependencies

Install packages needed in notebooks:

```bash
uv add numpy pandas scikit-learn matplotlib
```

## Using in notebooks

Access your project code:

```python
import sys
sys.path.insert(0, '../src')

from mymodule import my_function
```

## Virtual environment activation

uv automatically manages the environment. Just run:

```bash
uv run jupyter notebook
```

## Jupyter extensions

Install Jupyter extensions:

```bash
uv add jupyterlab-code-formatter ipywidgets
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/integration-jupyter/
