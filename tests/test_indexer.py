# tests/test_indexer.py
import tempfile
from pathlib import Path

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
