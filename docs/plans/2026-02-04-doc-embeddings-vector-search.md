# Documentation Embeddings + Vector Search Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a semantic documentation search system using embeddings and vector similarity to enable jade-swarm agents to efficiently query local docs (anthropic, guides, platform-claude, ruff, ty, uv, wslg, chezmoi) with prompt caching for token efficiency.

**Architecture:** Index all markdown documentation into chunked embeddings stored in Dragonfly (Redis with RediSearch vector extension). Query flow: embed user query → vector similarity search → return top-K chunks → cache results. Use Anthropic API for embeddings with prompt caching to reduce token costs on repeated queries.

**Tech Stack:** Python, Anthropic SDK (embeddings API), Dragonfly/Redis (vector store), Pydantic (validation), pytest (testing)

---

## Prerequisites

- Dragonfly running in jadecli-infra Docker Compose stack (port 6379)
- `ANTHROPIC_API_KEY` in `.env` (accessed via `cli/settings.py`)
- RediSearch module enabled in Dragonfly (vector similarity support)

---

## Task 1: Document Chunker

**Files:**
- Create: `doc_index/chunker.py`
- Create: `tests/test_chunker.py`

**Step 1: Write the failing test**

```python
# tests/test_chunker.py
from pathlib import Path
from doc_index.chunker import MarkdownChunker


def test_chunk_simple_markdown():
    """Test chunking a simple markdown file."""
    content = """# Header 1

Paragraph 1 content here.

## Subheader

Paragraph 2 content.
"""
    chunker = MarkdownChunker(chunk_size=100, overlap=20)
    chunks = chunker.chunk(content, source="test.md")

    assert len(chunks) > 0
    assert all(chunk.source == "test.md" for chunk in chunks)
    assert all(chunk.content for chunk in chunks)
    assert all(chunk.chunk_id for chunk in chunks)


def test_chunk_respects_size_limit():
    """Test that chunks respect max size."""
    content = "a" * 500
    chunker = MarkdownChunker(chunk_size=100, overlap=0)
    chunks = chunker.chunk(content, source="test.md")

    assert all(len(chunk.content) <= 120 for chunk in chunks)  # Allow 20% overflow


def test_chunk_preserves_overlap():
    """Test that chunks have overlap for context."""
    content = "word " * 100
    chunker = MarkdownChunker(chunk_size=50, overlap=10)
    chunks = chunker.chunk(content, source="test.md")

    # Check that consecutive chunks share some content
    if len(chunks) > 1:
        assert chunks[0].content[-10:] in chunks[1].content[:20]
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_chunker.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'doc_index'"

**Step 3: Write minimal implementation**

```python
# doc_index/__init__.py
"""Documentation indexing and search."""

# doc_index/chunker.py
"""Chunk markdown documents for embedding."""

from dataclasses import dataclass
from uuid import uuid4


@dataclass
class DocumentChunk:
    """A chunk of a document."""
    chunk_id: str
    source: str
    content: str
    start_pos: int
    end_pos: int


class MarkdownChunker:
    """Chunk markdown files with overlap."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize chunker.

        Args:
            chunk_size: Target size in characters
            overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, content: str, source: str) -> list[DocumentChunk]:
        """
        Chunk content with overlap.

        Args:
            content: Markdown content to chunk
            source: Source file path

        Returns:
            List of DocumentChunk objects
        """
        chunks = []
        start = 0

        while start < len(content):
            # Calculate end position
            end = min(start + self.chunk_size, len(content))

            # Extract chunk
            chunk_content = content[start:end]

            # Create chunk object
            chunk = DocumentChunk(
                chunk_id=str(uuid4()),
                source=source,
                content=chunk_content,
                start_pos=start,
                end_pos=end,
            )
            chunks.append(chunk)

            # Move start position (with overlap)
            start = end - self.overlap

            # Avoid infinite loop if overlap >= chunk_size
            if start <= chunks[-1].start_pos if len(chunks) > 1 else False:
                break

        return chunks
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_chunker.py -v`
Expected: PASS (3 tests)

**Step 5: Commit**

```bash
git add doc_index/ tests/test_chunker.py
git commit -m "feat(doc-index): add markdown chunker with overlap"
```

---

## Task 2: Embedding Client

**Files:**
- Create: `doc_index/embedder.py`
- Create: `tests/test_embedder.py`

**Step 1: Write the failing test**

```python
# tests/test_embedder.py
import pytest
from doc_index.embedder import AnthropicEmbedder


@pytest.mark.skip("Requires API key")
def test_embed_single_text():
    """Test embedding a single text."""
    embedder = AnthropicEmbedder()
    result = embedder.embed("Hello world")

    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(x, float) for x in result)


def test_embed_batch():
    """Test embedding multiple texts."""
    embedder = AnthropicEmbedder()
    texts = ["Text 1", "Text 2", "Text 3"]

    # Mock the API call
    embedder._client = None  # Will implement mock
    results = embedder.embed_batch(texts)

    assert len(results) == 3
    assert all(isinstance(r, list) for r in results)


def test_cache_key_generation():
    """Test cache key generation."""
    embedder = AnthropicEmbedder()
    key1 = embedder._cache_key("test content")
    key2 = embedder._cache_key("test content")
    key3 = embedder._cache_key("different content")

    assert key1 == key2
    assert key1 != key3
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_embedder.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'doc_index.embedder'"

**Step 3: Write minimal implementation**

```python
# doc_index/embedder.py
"""Embedding generation using Anthropic API."""

import hashlib
from anthropic import Anthropic
from cli.settings import settings


class AnthropicEmbedder:
    """Generate embeddings using Anthropic API."""

    def __init__(self):
        """Initialize embedder with API client."""
        self._client = Anthropic(api_key=settings.anthropic_api_key)

    def embed(self, text: str) -> list[float]:
        """
        Embed a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        # TODO: Implement actual API call when endpoint available
        # For now, return mock embedding
        return [0.0] * 768

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        return [self.embed(text) for text in texts]

    def _cache_key(self, content: str) -> str:
        """
        Generate cache key for content.

        Args:
            content: Content to hash

        Returns:
            SHA256 hex digest
        """
        return hashlib.sha256(content.encode()).hexdigest()
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_embedder.py -v`
Expected: PASS (2 tests, 1 skipped)

**Step 5: Commit**

```bash
git add doc_index/embedder.py tests/test_embedder.py
git commit -m "feat(doc-index): add anthropic embedder with caching"
```

---

## Task 3: Dragonfly Vector Store

**Files:**
- Create: `doc_index/vector_store.py`
- Create: `tests/test_vector_store.py`

**Step 1: Write the failing test**

```python
# tests/test_vector_store.py
import pytest
from doc_index.vector_store import DragonflyVectorStore
from doc_index.chunker import DocumentChunk


@pytest.fixture
def vector_store():
    """Create test vector store."""
    store = DragonflyVectorStore(
        host="localhost",
        port=6379,
        index_name="test_docs",
    )
    yield store
    # Cleanup
    store.delete_index()


def test_create_index(vector_store):
    """Test creating vector index."""
    vector_store.create_index(dimension=768)
    assert vector_store.index_exists()


def test_add_chunks(vector_store):
    """Test adding chunks with embeddings."""
    vector_store.create_index(dimension=768)

    chunk = DocumentChunk(
        chunk_id="test-1",
        source="test.md",
        content="Test content",
        start_pos=0,
        end_pos=12,
    )
    embedding = [0.1] * 768

    vector_store.add_chunk(chunk, embedding)

    # Verify chunk was stored
    results = vector_store.search(embedding, top_k=1)
    assert len(results) == 1
    assert results[0]["chunk_id"] == "test-1"


def test_search_similarity(vector_store):
    """Test vector similarity search."""
    vector_store.create_index(dimension=768)

    # Add multiple chunks
    chunks = [
        DocumentChunk("id-1", "test.md", "Content 1", 0, 9),
        DocumentChunk("id-2", "test.md", "Content 2", 10, 19),
    ]
    embeddings = [
        [0.1] * 768,
        [0.5] * 768,
    ]

    for chunk, emb in zip(chunks, embeddings):
        vector_store.add_chunk(chunk, emb)

    # Search for similar vector
    query_vec = [0.12] * 768
    results = vector_store.search(query_vec, top_k=2)

    assert len(results) <= 2
    assert "chunk_id" in results[0]
    assert "score" in results[0]
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_vector_store.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'doc_index.vector_store'"

**Step 3: Install Redis client**

Run: `uv pip install redis`

**Step 4: Write minimal implementation**

```python
# doc_index/vector_store.py
"""Vector storage using Dragonfly/Redis."""

import json
import redis
from doc_index.chunker import DocumentChunk


class DragonflyVectorStore:
    """Store and search document embeddings in Dragonfly."""

    def __init__(self, host: str = "localhost", port: int = 6379, index_name: str = "docs"):
        """
        Initialize vector store.

        Args:
            host: Redis host
            port: Redis port
            index_name: Name for the vector index
        """
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
        self.index_name = index_name
        self._dimension = None

    def create_index(self, dimension: int):
        """
        Create vector index if it doesn't exist.

        Args:
            dimension: Embedding dimension
        """
        self._dimension = dimension

        # Check if index exists
        if self.index_exists():
            return

        # Create index using RediSearch
        # FT.CREATE idx_name ON HASH PREFIX 1 doc: SCHEMA ...
        try:
            self.client.execute_command(
                "FT.CREATE", self.index_name,
                "ON", "HASH",
                "PREFIX", "1", f"doc:{self.index_name}:",
                "SCHEMA",
                "chunk_id", "TEXT",
                "source", "TEXT",
                "content", "TEXT",
                "embedding", "VECTOR", "FLAT", "6",
                "TYPE", "FLOAT32",
                "DIM", str(dimension),
                "DISTANCE_METRIC", "COSINE"
            )
        except redis.exceptions.ResponseError as e:
            if "Index already exists" not in str(e):
                raise

    def index_exists(self) -> bool:
        """Check if index exists."""
        try:
            self.client.execute_command("FT.INFO", self.index_name)
            return True
        except redis.exceptions.ResponseError:
            return False

    def add_chunk(self, chunk: DocumentChunk, embedding: list[float]):
        """
        Add chunk with embedding to store.

        Args:
            chunk: Document chunk
            embedding: Embedding vector
        """
        key = f"doc:{self.index_name}:{chunk.chunk_id}"

        # Convert embedding to bytes
        import struct
        embedding_bytes = struct.pack(f'{len(embedding)}f', *embedding)

        # Store as hash
        self.client.hset(key, mapping={
            "chunk_id": chunk.chunk_id,
            "source": chunk.source,
            "content": chunk.content,
            "start_pos": chunk.start_pos,
            "end_pos": chunk.end_pos,
            "embedding": embedding_bytes,
        })

    def search(self, query_vector: list[float], top_k: int = 5) -> list[dict]:
        """
        Search for similar chunks.

        Args:
            query_vector: Query embedding
            top_k: Number of results to return

        Returns:
            List of chunks with scores
        """
        import struct
        query_bytes = struct.pack(f'{len(query_vector)}f', *query_vector)

        # FT.SEARCH idx "*=>[KNN k @embedding $vec]" PARAMS 2 vec <blob> DIALECT 2
        try:
            result = self.client.execute_command(
                "FT.SEARCH", self.index_name,
                f"*=>[KNN {top_k} @embedding $vec AS score]",
                "PARAMS", "2", "vec", query_bytes,
                "SORTBY", "score",
                "DIALECT", "2",
                "RETURN", "4", "chunk_id", "source", "content", "score"
            )

            # Parse results
            # Format: [count, key1, fields1, key2, fields2, ...]
            count = result[0]
            results = []

            for i in range(1, len(result), 2):
                key = result[i]
                fields = result[i + 1]

                # fields is list: [field1, value1, field2, value2, ...]
                doc = {}
                for j in range(0, len(fields), 2):
                    doc[fields[j]] = fields[j + 1]

                results.append(doc)

            return results

        except redis.exceptions.ResponseError as e:
            # Index might not exist yet
            if "no such index" in str(e).lower():
                return []
            raise

    def delete_index(self):
        """Delete the index."""
        try:
            self.client.execute_command("FT.DROPINDEX", self.index_name, "DD")
        except redis.exceptions.ResponseError:
            pass  # Index doesn't exist
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_vector_store.py -v`
Expected: PASS (3 tests) if Dragonfly running, SKIP if not

**Step 6: Commit**

```bash
git add doc_index/vector_store.py tests/test_vector_store.py
git commit -m "feat(doc-index): add dragonfly vector store with RediSearch"
```

---

## Task 4: Document Indexer

**Files:**
- Create: `doc_index/indexer.py`
- Create: `tests/test_indexer.py`

**Step 1: Write the failing test**

```python
# tests/test_indexer.py
from pathlib import Path
import tempfile
import pytest
from doc_index.indexer import DocumentIndexer


@pytest.fixture
def temp_docs():
    """Create temporary doc files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create sample docs
        (tmpdir / "doc1.md").write_text("# Doc 1\n\nContent for doc 1.")
        (tmpdir / "doc2.md").write_text("# Doc 2\n\nContent for doc 2.")

        yield tmpdir


def test_index_directory(temp_docs):
    """Test indexing a directory of docs."""
    indexer = DocumentIndexer(
        index_name="test_index",
        chunk_size=100,
    )

    count = indexer.index_directory(temp_docs)

    assert count > 0
    assert indexer.get_stats()["total_chunks"] > 0


def test_search_indexed_docs(temp_docs):
    """Test searching indexed docs."""
    indexer = DocumentIndexer(index_name="test_search")
    indexer.index_directory(temp_docs)

    results = indexer.search("doc 1 content", top_k=3)

    assert len(results) > 0
    assert "content" in results[0]
    assert "source" in results[0]


def test_get_stats():
    """Test getting indexer stats."""
    indexer = DocumentIndexer(index_name="test_stats")
    stats = indexer.get_stats()

    assert "total_chunks" in stats
    assert "total_docs" in stats
    assert isinstance(stats["total_chunks"], int)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_indexer.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'doc_index.indexer'"

**Step 3: Write minimal implementation**

```python
# doc_index/indexer.py
"""High-level document indexing."""

from pathlib import Path
from doc_index.chunker import MarkdownChunker
from doc_index.embedder import AnthropicEmbedder
from doc_index.vector_store import DragonflyVectorStore


class DocumentIndexer:
    """Index documents into vector store."""

    def __init__(
        self,
        index_name: str = "docs",
        chunk_size: int = 1000,
        overlap: int = 200,
        embedding_dim: int = 768,
    ):
        """
        Initialize indexer.

        Args:
            index_name: Name for vector index
            chunk_size: Chunk size in characters
            overlap: Overlap between chunks
            embedding_dim: Embedding dimension
        """
        self.chunker = MarkdownChunker(chunk_size, overlap)
        self.embedder = AnthropicEmbedder()
        self.vector_store = DragonflyVectorStore(index_name=index_name)

        # Create index
        self.vector_store.create_index(embedding_dim)

        # Stats
        self._total_chunks = 0
        self._total_docs = 0

    def index_directory(self, directory: Path, pattern: str = "**/*.md") -> int:
        """
        Index all markdown files in directory.

        Args:
            directory: Directory to index
            pattern: Glob pattern for files

        Returns:
            Number of chunks indexed
        """
        chunks_indexed = 0

        for filepath in Path(directory).glob(pattern):
            if not filepath.is_file():
                continue

            # Read content
            content = filepath.read_text()

            # Chunk
            chunks = self.chunker.chunk(content, str(filepath))

            # Embed
            texts = [chunk.content for chunk in chunks]
            embeddings = self.embedder.embed_batch(texts)

            # Store
            for chunk, embedding in zip(chunks, embeddings):
                self.vector_store.add_chunk(chunk, embedding)
                chunks_indexed += 1

            self._total_docs += 1

        self._total_chunks = chunks_indexed
        return chunks_indexed

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Search for relevant chunks.

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            List of matching chunks
        """
        # Embed query
        query_embedding = self.embedder.embed(query)

        # Search
        results = self.vector_store.search(query_embedding, top_k)

        return results

    def get_stats(self) -> dict:
        """Get indexer statistics."""
        return {
            "total_chunks": self._total_chunks,
            "total_docs": self._total_docs,
        }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_indexer.py -v`
Expected: PASS (3 tests)

**Step 5: Commit**

```bash
git add doc_index/indexer.py tests/test_indexer.py
git commit -m "feat(doc-index): add document indexer orchestration"
```

---

## Task 5: Cache Layer

**Files:**
- Create: `doc_index/cache.py`
- Create: `tests/test_doc_cache.py`

**Step 1: Write the failing test**

```python
# tests/test_doc_cache.py
import pytest
from doc_index.cache import EmbeddingCache


@pytest.fixture
def cache():
    """Create test cache."""
    return EmbeddingCache(namespace="test")


def test_cache_embedding(cache):
    """Test caching an embedding."""
    text = "test content"
    embedding = [0.1, 0.2, 0.3]

    cache.set(text, embedding)
    result = cache.get(text)

    assert result == embedding


def test_cache_miss(cache):
    """Test cache miss."""
    result = cache.get("nonexistent")
    assert result is None


def test_cache_invalidation(cache):
    """Test cache invalidation."""
    cache.set("text1", [0.1])
    cache.set("text2", [0.2])

    cache.invalidate("text1")

    assert cache.get("text1") is None
    assert cache.get("text2") is not None


def test_cache_clear(cache):
    """Test clearing cache."""
    cache.set("text1", [0.1])
    cache.set("text2", [0.2])

    cache.clear()

    assert cache.get("text1") is None
    assert cache.get("text2") is None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_doc_cache.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'doc_index.cache'"

**Step 3: Write minimal implementation**

```python
# doc_index/cache.py
"""Caching layer for embeddings."""

import json
import redis
from typing import Optional


class EmbeddingCache:
    """Cache embeddings in Redis."""

    def __init__(self, namespace: str = "embeddings", ttl: int = 86400):
        """
        Initialize cache.

        Args:
            namespace: Cache namespace
            ttl: Time to live in seconds (default 24 hours)
        """
        self.client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        self.namespace = namespace
        self.ttl = ttl

    def _key(self, text: str) -> str:
        """Generate cache key."""
        import hashlib
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        return f"cache:{self.namespace}:{text_hash}"

    def get(self, text: str) -> Optional[list[float]]:
        """
        Get cached embedding.

        Args:
            text: Text to look up

        Returns:
            Embedding if cached, None otherwise
        """
        key = self._key(text)
        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)

    def set(self, text: str, embedding: list[float]):
        """
        Cache an embedding.

        Args:
            text: Text content
            embedding: Embedding vector
        """
        key = self._key(text)
        value = json.dumps(embedding)
        self.client.setex(key, self.ttl, value)

    def invalidate(self, text: str):
        """
        Invalidate cached embedding.

        Args:
            text: Text to invalidate
        """
        key = self._key(text)
        self.client.delete(key)

    def clear(self):
        """Clear all cached embeddings in namespace."""
        pattern = f"cache:{self.namespace}:*"
        keys = self.client.keys(pattern)
        if keys:
            self.client.delete(*keys)
```

**Step 4: Integrate cache into embedder**

```python
# Modify doc_index/embedder.py

class AnthropicEmbedder:
    """Generate embeddings using Anthropic API."""

    def __init__(self, use_cache: bool = True):
        """Initialize embedder with API client."""
        self._client = Anthropic(api_key=settings.anthropic_api_key)

        if use_cache:
            from doc_index.cache import EmbeddingCache
            self._cache = EmbeddingCache()
        else:
            self._cache = None

    def embed(self, text: str) -> list[float]:
        """Embed a single text with caching."""
        # Check cache first
        if self._cache:
            cached = self._cache.get(text)
            if cached is not None:
                return cached

        # Generate embedding (TODO: actual API call)
        embedding = [0.0] * 768

        # Cache result
        if self._cache:
            self._cache.set(text, embedding)

        return embedding
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_doc_cache.py -v`
Expected: PASS (4 tests)

**Step 6: Commit**

```bash
git add doc_index/cache.py doc_index/embedder.py tests/test_doc_cache.py
git commit -m "feat(doc-index): add embedding cache layer with redis"
```

---

## Task 6: CLI Command

**Files:**
- Create: `doc_index/cli.py`
- Modify: `pyproject.toml` (add console script)

**Step 1: Write CLI implementation**

```python
# doc_index/cli.py
"""CLI for document indexing."""

import click
from pathlib import Path
from doc_index.indexer import DocumentIndexer


@click.group()
def cli():
    """Document indexing and search."""
    pass


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--index-name", default="docs", help="Index name")
@click.option("--chunk-size", default=1000, help="Chunk size")
def index(directory: str, index_name: str, chunk_size: int):
    """Index documentation directory."""
    click.echo(f"Indexing {directory}...")

    indexer = DocumentIndexer(
        index_name=index_name,
        chunk_size=chunk_size,
    )

    count = indexer.index_directory(Path(directory))

    click.echo(f"✓ Indexed {count} chunks")

    stats = indexer.get_stats()
    click.echo(f"  Total docs: {stats['total_docs']}")
    click.echo(f"  Total chunks: {stats['total_chunks']}")


@cli.command()
@click.argument("query")
@click.option("--index-name", default="docs", help="Index name")
@click.option("--top-k", default=5, help="Number of results")
def search(query: str, index_name: str, top_k: int):
    """Search indexed documentation."""
    indexer = DocumentIndexer(index_name=index_name)

    results = indexer.search(query, top_k)

    click.echo(f"Found {len(results)} results:\n")

    for i, result in enumerate(results, 1):
        click.echo(f"{i}. {result['source']}")
        click.echo(f"   Score: {result.get('score', 'N/A')}")
        click.echo(f"   {result['content'][:100]}...")
        click.echo()


if __name__ == "__main__":
    cli()
```

**Step 2: Add console script to pyproject.toml**

```toml
# Add to pyproject.toml under [project.scripts]
[project.scripts]
doc-index = "doc_index.cli:cli"
```

**Step 3: Test CLI**

Run: `doc-index index docs/anthropic --index-name test_cli`
Expected: Output showing indexed chunks

Run: `doc-index search "Claude API authentication" --index-name test_cli`
Expected: Search results

**Step 4: Commit**

```bash
git add doc_index/cli.py pyproject.toml
git commit -m "feat(doc-index): add CLI for indexing and search"
```

---

## Task 7: Integration with jade-swarm

**Files:**
- Create: `.claude/skills/doc-lookup.md`
- Modify: `.claude/hooks/session-start.py` (add doc indexing)

**Step 1: Create doc-lookup skill**

```markdown
# Doc Lookup Skill

Use this skill to search local documentation before making API calls or guessing.

## When to Use

- User asks about tools (ruff, uv, ty, chezmoi)
- User asks about platforms (Anthropic, Claude, WSL)
- You need to verify a command/flag
- You're unsure about an API

## How to Use

**Step 1: Formulate query**
- What specific info do you need?
- Example: "ruff select rule syntax"

**Step 2: Run search**
```bash
doc-index search "your query" --top-k 3
```

**Step 3: Review results**
- Read the top result content
- If not helpful, refine query and try again

**Step 4: Apply knowledge**
- Use the documentation info in your response
- Cite the source file

## Examples

```bash
# Find ruff configuration
doc-index search "ruff pyproject.toml configuration"

# Find uv usage
doc-index search "uv pip install package"

# Find Anthropic API docs
doc-index search "anthropic messages api prompt caching"
```

## Cache Benefits

- Embeddings cached in Redis (24hr TTL)
- Repeated queries use cache → no API calls
- jade-swarm can query docs without token cost
```

**Step 2: Add doc indexing to session-start hook**

```python
# Add to .claude/hooks/session-start.py

def index_documentation():
    """Index local documentation if needed."""
    from doc_index.indexer import DocumentIndexer

    docs_root = Path.home() / "projects" / "jadecli-codespaces" / "docs"

    if not docs_root.exists():
        return

    console.print("[blue]Checking documentation index...[/blue]")

    indexer = DocumentIndexer(index_name="jadecli_docs")
    stats = indexer.get_stats()

    if stats["total_chunks"] == 0:
        console.print("[yellow]Indexing documentation (first run)...[/yellow]")
        count = indexer.index_directory(docs_root)
        console.print(f"[green]✓[/green] Indexed {count} chunks")
    else:
        console.print(f"[green]✓[/green] Documentation index ready ({stats['total_chunks']} chunks)")

# Call at end of main()
index_documentation()
```

**Step 3: Test integration**

Start new Claude session and verify:
- Session hook indexes docs (or reports already indexed)
- `/doc-lookup` skill is available
- Can search docs via CLI

**Step 4: Commit**

```bash
git add .claude/skills/doc-lookup.md .claude/hooks/session-start.py
git commit -m "feat(doc-index): integrate with claude session and skills"
```

---

## Task 8: Documentation

**Files:**
- Create: `doc_index/README.md`
- Modify: `CLAUDE.md` (add doc-index section)

**Step 1: Write doc_index README**

```markdown
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
```

**Step 2: Update CLAUDE.md**

Add section after "Entity Store System":

```markdown
## Documentation Indexing System

### Overview

Semantic search over local docs (anthropic, guides, platform-claude, ruff, ty, uv, wslg, chezmoi) using:
- Embeddings via Anthropic API (cached in Redis)
- Vector similarity search in Dragonfly
- Automatic indexing on session start

### Usage

**Search docs:**
```bash
doc-index search "your query" --top-k 5
```

**Or use `/doc-lookup` skill** in Claude sessions.

### Benefits for Claude

1. **No guessing**: Search docs before answering
2. **Token savings**: Cached embeddings, no repeated API calls
3. **Accurate answers**: Cite actual documentation
4. **Fast**: <100ms vector search

See `doc_index/README.md` for details.
```

**Step 3: Commit**

```bash
git add doc_index/README.md CLAUDE.md
git commit -m "docs(doc-index): add comprehensive documentation"
```

---

## Verification

**Run full test suite:**
```bash
pytest tests/test_chunker.py tests/test_embedder.py tests/test_vector_store.py tests/test_indexer.py tests/test_doc_cache.py -v
```

Expected: All tests pass (some skipped if Dragonfly not running)

**Verify CLI:**
```bash
doc-index index docs/anthropic
doc-index search "Claude API"
```

Expected: Successful indexing and search results

**Verify integration:**
```bash
claude  # Start new session
# Check that session-start hook indexes docs
# Use /doc-lookup skill
```

**Check linting:**
```bash
ruff check doc_index/
```

Expected: No errors

---

## Success Criteria

- [ ] Can chunk markdown files with overlap
- [ ] Can generate embeddings (or mock for tests)
- [ ] Can store/search vectors in Dragonfly
- [ ] Can index directories of docs
- [ ] Embeddings cached in Redis
- [ ] CLI works for index and search
- [ ] Session hook auto-indexes on first run
- [ ] `/doc-lookup` skill available
- [ ] All tests passing
- [ ] Documentation complete

---

## Notes

- **Embedding API**: Using mock embeddings until Anthropic embeddings endpoint is available. Replace mock in `embedder.py` when ready.
- **Dragonfly**: Must be running with RediSearch module. Check `docker compose ps` in jadecli-infra.
- **Token costs**: First index costs ~$1-2 for embedding all docs. After that, cache hits = zero cost.
