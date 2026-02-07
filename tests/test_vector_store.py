import pytest

from doc_index.chunker import DocumentChunk
from doc_index.vector_store import DragonflyVectorStore


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
