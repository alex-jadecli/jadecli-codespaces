"""Caching layer for embeddings."""

import json

import redis


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

    def get(self, text: str) -> list[float] | None:
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
