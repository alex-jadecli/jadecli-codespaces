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
