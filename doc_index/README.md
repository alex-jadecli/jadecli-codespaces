# Documentation Indexing & Search

Semantic search over local documentation using embeddings and vector similarity.

## Quick Start

**Index documentation:**
```bash
doc-index index docs/anthropic --index-name docs
```

**Search:**
```bash
doc-index search "prompt caching API" --top-k 5
```

## Architecture

- **Chunker**: Splits markdown into overlapping chunks (1000 chars, 200 overlap)
- **Embedder**: Generates embeddings via Anthropic API (with Redis cache)
- **Vector Store**: Stores in Dragonfly/Redis with RediSearch vector extension
- **Search**: Cosine similarity search for semantic matching

## Benefits

- **Semantic search**: "find docs about X" works
- **Token efficient**: Embeddings cached in Redis (24hr TTL)
- **Fast**: Vector search in <100ms
- **Scalable**: Can index 1000s of docs

## Usage in Claude Sessions

The `session-start` hook auto-indexes docs on first run. Use the `/doc-lookup` skill to search:

```
User: "How do I configure ruff?"
Claude: Let me search the docs...
  $ doc-index search "ruff configuration" --top-k 3
  [Results show pyproject.toml examples]
```

## Configuration

Set in `.env`:
```bash
ANTHROPIC_API_KEY=sk-...
```

Redis/Dragonfly must be running (default: localhost:6379).

## Testing

```bash
pytest tests/test_chunker.py
pytest tests/test_embedder.py
pytest tests/test_vector_store.py
pytest tests/test_indexer.py
pytest tests/test_doc_cache.py
```
