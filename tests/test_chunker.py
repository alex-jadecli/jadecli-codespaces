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
