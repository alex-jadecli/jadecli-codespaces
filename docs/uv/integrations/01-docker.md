# Docker Integration

Using uv in Docker images.

## Basic Docker setup

Create a Dockerfile with uv:

```dockerfile
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml uv.lock /app/
WORKDIR /app

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY src/ src/

# Set environment
ENV PATH="/app/.venv/bin:$PATH"

# Run application
CMD ["python", "-m", "myapp"]
```

## Using uv official image

Use the official uv Docker image:

```dockerfile
FROM ghcr.io/astral-sh/uv:latest

COPY pyproject.toml uv.lock /app/
WORKDIR /app

RUN uv sync --frozen

COPY . .

CMD ["uv", "run", "main.py"]
```

## Multi-stage builds

Optimize image size with multi-stage builds:

```dockerfile
FROM ghcr.io/astral-sh/uv:latest as builder

COPY pyproject.toml uv.lock /app/
WORKDIR /app

RUN uv sync --frozen --no-dev

FROM python:3.12-slim

COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app

CMD ["python", "-m", "myapp"]
```

## Docker compose

Use uv in docker-compose.yml:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - UV_INDEX_URL=https://pypi.org/simple/
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/integration-docker/
