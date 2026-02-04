# ---
# entity_id: module-neon-client
# entity_name: Neon PostgreSQL Client
# entity_type_id: module
# entity_path: entity_store/neon_client.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: [NeonClient]
# entity_dependencies: [models]
# ---

"""
Neon PostgreSQL client for entity storage.

Provides async database operations for:
- Entity CRUD
- Full-text search (BM25)
- Query caching
- Change tracking
"""

from datetime import datetime
from uuid import UUID

from entity_store.models import Entity


class NeonClient:
    """
    Async client for Neon PostgreSQL via MCP.

    Handles all database operations including:
    - Entity upsert with conflict resolution
    - BM25 full-text search
    - Query result caching
    - Change log for cache invalidation
    """

    def __init__(self, connection_string: str | None = None) -> None:
        """
        Initialize Neon client.

        Args:
            connection_string: PostgreSQL connection string.
                              If None, uses MCP server.
        """
        self.connection_string = connection_string
        self._connected = False

    async def connect(self) -> None:
        """Establish connection to Neon PostgreSQL."""
        raise NotImplementedError("connect not yet implemented")

    async def disconnect(self) -> None:
        """Close connection to Neon PostgreSQL."""
        raise NotImplementedError("disconnect not yet implemented")

    async def upsert_entity(self, entity: Entity) -> UUID:
        """
        Upsert an entity (insert or update on conflict).

        Args:
            entity: Entity to upsert

        Returns:
            UUID of the upserted entity
        """
        raise NotImplementedError("upsert_entity not yet implemented")

    async def get_entity(self, entity_id: UUID) -> Entity | None:
        """
        Get an entity by ID.

        Args:
            entity_id: UUID of the entity

        Returns:
            Entity if found, None otherwise
        """
        raise NotImplementedError("get_entity not yet implemented")

    async def search_entities(self, query: str, limit: int = 20) -> list[Entity]:
        """
        Search entities using BM25 full-text search.

        Args:
            query: Search query text
            limit: Maximum results to return

        Returns:
            List of matching entities ranked by relevance
        """
        raise NotImplementedError("search_entities not yet implemented")

    async def get_last_index_time(self, repo_path: str) -> datetime | None:
        """
        Get the last indexing time for a repository.

        Args:
            repo_path: Path to the repository

        Returns:
            Last index time or None if never indexed
        """
        raise NotImplementedError("get_last_index_time not yet implemented")

    async def set_last_index_time(self, repo_path: str) -> None:
        """
        Update the last indexing time for a repository.

        Args:
            repo_path: Path to the repository
        """
        raise NotImplementedError("set_last_index_time not yet implemented")

    async def log_change(
        self,
        entity_id: UUID,
        entity_path: str,
        change_type: str,
        old_signature: str | None = None,
        new_signature: str | None = None,
    ) -> None:
        """
        Log an entity change for cache invalidation.

        Args:
            entity_id: UUID of the changed entity
            entity_path: Path to the entity file
            change_type: Type of change (create, update, delete)
            old_signature: Previous signature (for updates)
            new_signature: New signature (for creates/updates)
        """
        raise NotImplementedError("log_change not yet implemented")
