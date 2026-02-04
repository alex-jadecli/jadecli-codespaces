# ---
# entity_id: module-graphql-query
# entity_name: GraphQL-like Query Interface
# entity_type_id: module
# entity_path: entity_store/query/graphql.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: [EntityQuery, QueryResult]
# entity_dependencies: [models, registry]
# ---

"""
GraphQL-like query interface for entities.

Provides a flexible query API that reduces token usage:
- Field projection (only return requested fields)
- Filters (type, name, path, state)
- Pagination (limit, offset)
- Sorting (by field, direction)
"""

from dataclasses import dataclass
from typing import Any

from entity_store.models import Entity
from entity_store.registry import EntityRegistry


@dataclass
class QueryResult:
    """Result of an entity query."""

    entities: list[dict[str, Any]]
    total_count: int
    has_more: bool


class EntityQuery:
    """
    GraphQL-like query interface for entities.

    Enables efficient queries with field projection
    to minimize token usage in Claude responses.
    """

    def __init__(self, registry: EntityRegistry) -> None:
        """
        Initialize query interface.

        Args:
            registry: Entity registry for data access
        """
        self.registry = registry

    def query(
        self,
        type_id: str | None = None,
        name_pattern: str | None = None,
        path_pattern: str | None = None,
        state: str = "active",
        fields: list[str] | None = None,
        limit: int = 100,
        offset: int = 0,
        order_by: str | None = None,
        order_desc: bool = False,
    ) -> QueryResult:
        """
        Query entities with optional field projection.

        Args:
            type_id: Filter by entity type (class, function, etc.)
            name_pattern: Filter by name pattern (glob)
            path_pattern: Filter by path pattern (glob)
            state: Filter by state (active, deprecated, archived)
            fields: List of fields to return (projection)
            limit: Maximum results to return
            offset: Number of results to skip
            order_by: Field to sort by
            order_desc: Sort descending if True

        Returns:
            QueryResult with projected entity data

        Example:
            query(type_id="class", fields=["entity_name", "entity_path"])
        """
        raise NotImplementedError("query not yet implemented")

    def search(
        self,
        query_text: str,
        fields: list[str] | None = None,
        limit: int = 20,
    ) -> QueryResult:
        """
        Full-text search across entities.

        Args:
            query_text: Search query
            fields: List of fields to return
            limit: Maximum results

        Returns:
            QueryResult ranked by relevance
        """
        raise NotImplementedError("search not yet implemented")

    def get_hierarchy(
        self,
        root_id: str,
        max_depth: int = 10,
        fields: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get entity hierarchy starting from root.

        Args:
            root_id: UUID of root entity
            max_depth: Maximum hierarchy depth
            fields: List of fields to return

        Returns:
            List of entities with depth information
        """
        raise NotImplementedError("get_hierarchy not yet implemented")

    def _project_fields(self, entity: Entity, fields: list[str]) -> dict[str, Any]:
        """
        Project only requested fields from entity.

        Args:
            entity: Entity to project
            fields: Fields to include

        Returns:
            Dict with only requested fields
        """
        entity_dict = entity.model_dump()
        return {f: entity_dict[f] for f in fields if f in entity_dict}

    def _apply_filters(
        self,
        entities: list[Entity],
        type_id: str | None,
        name_pattern: str | None,
        path_pattern: str | None,
        state: str,
    ) -> list[Entity]:
        """Apply filters to entity list."""
        raise NotImplementedError("_apply_filters not yet implemented")
