# GitHub Actions Integration

Using uv in GitHub Actions CI/CD.

## Installing uv in Actions

Use the official setup action:

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v1
```

## Basic workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v1
      
      - name: Run tests
        run: uv run pytest
```

## Testing multiple Python versions

Test across versions:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12', '3.13']
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v1
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Run tests
        run: uv run pytest
```

## Linting and formatting

```yaml
- name: Lint
  run: uv run ruff check .

- name: Format check
  run: uv run black --check .
```

## Building and publishing

```yaml
- name: Build
  run: uv build

- name: Publish
  uses: pypa/gh-action-pypi-publish@release/v1
```

## Caching

Enable action caching:

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v1
  with:
    cache: true
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/integration-github-actions/
