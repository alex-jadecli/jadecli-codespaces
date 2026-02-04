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
