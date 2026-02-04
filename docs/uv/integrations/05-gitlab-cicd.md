# GitLab CI/CD Integration

Using uv in GitLab CI/CD pipelines.

## Basic setup

Create `.gitlab-ci.yml`:

```yaml
image: python:3.12

before_script:
  - curl -LsSf https://astral.sh/uv/install.sh | sh
  - export PATH="/root/.local/bin:$PATH"

test:
  script:
    - uv run pytest
```

## Installing uv in Docker image

Use a Docker image with uv pre-installed:

```yaml
image: ghcr.io/astral-sh/uv:latest

test:
  script:
    - uv run pytest
```

## Testing multiple versions

Test across Python versions:

```yaml
stages:
  - test

test:3.11:
  image: python:3.11
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="/root/.local/bin:$PATH"
  script:
    - uv run pytest

test:3.12:
  image: python:3.12
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="/root/.local/bin:$PATH"
  script:
    - uv run pytest

test:3.13:
  image: python:3.13
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="/root/.local/bin:$PATH"
  script:
    - uv run pytest
```

## Caching dependencies

```yaml
cache:
  paths:
    - .cache/uv/

test:
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="/root/.local/bin:$PATH"
    - export UV_CACHE_DIR=.cache/uv
  script:
    - uv run pytest
```

## Building and publishing

```yaml
build:
  script:
    - uv build

publish:
  script:
    - uvx twine upload dist/*
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/integration-gitlab/
