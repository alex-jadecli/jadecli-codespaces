# FastAPI Integration

Building FastAPI applications with uv.

## Project setup

Create a new FastAPI project:

```bash
uv init my-api --python 3.11
cd my-api
uv add fastapi uvicorn
```

## Basic FastAPI app

Create `src/main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

## Running the server

```bash
uv run uvicorn src.main:app --reload
```

## Project structure

Organize your FastAPI project:

```
my-api/
├── pyproject.toml
├── src/
│   ├── main.py
│   ├── models.py
│   └── routes/
│       ├── items.py
│       └── users.py
├── tests/
│   └── test_api.py
└── requirements.txt
```

## Development dependencies

Install dev tools:

```bash
uv add --dev pytest httpx black ruff mypy
```

## Testing

Create `tests/test_api.py`:

```python
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
```

Run tests:

```bash
uv run pytest
```

## Deployment

Create Docker setup for production:

```dockerfile
FROM ghcr.io/astral-sh/uv:latest

COPY pyproject.toml uv.lock /app/
WORKDIR /app

RUN uv sync --frozen --no-dev

COPY src/ src/

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0"]
```

## More Information

For complete details, visit: https://docs.astral.sh/uv/guides/fastapi/
