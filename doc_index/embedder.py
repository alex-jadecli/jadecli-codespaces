"""Embedding generation using Anthropic API."""

import hashlib

from anthropic import Anthropic

from cli.settings import settings


class AnthropicEmbedder:
    """Generate embeddings using Anthropic API."""

    def __init__(self, use_cache: bool = True):
        """
        Initialize embedder with API client.

        Args:
            use_cache: Whether to use Redis caching for embeddings
        """
        self._client = Anthropic(api_key=settings.anthropic_api_key)

        if use_cache:
            from doc_index.cache import EmbeddingCache

            self._cache = EmbeddingCache()
        else:
            self._cache = None

    def embed(self, text: str) -> list[float]:
        """
        Embed a single text with caching.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        # Check cache first
        if self._cache:
            cached = self._cache.get(text)
            if cached is not None:
                return cached

        # Generate embedding (TODO: actual API call when endpoint available)
        # For now, return mock embedding
        embedding = [0.0] * 768

        # Cache result
        if self._cache:
            self._cache.set(text, embedding)

        return embedding

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
