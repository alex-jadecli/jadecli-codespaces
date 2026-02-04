# ---
# entity_id: module-registry
# entity_name: Entity Registry
# entity_type_id: module
# entity_path: entity_store/registry.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: [EntityRegistry]
# entity_dependencies: [models, neon_client, parsers, frontmatter]
# ---

"""
Entity Registry - CRUD operations for entities.

Provides the main interface for:
- Registering new entities from parsed AST
- Querying entities by type, path, name
- Updating entity state and metadata
- Deleting/archiving entities
- Locking/unlocking entities for multi-agent collaboration
"""

from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

from entity_store.frontmatter import (
    EntityFrontmatter,
    EntityTypeId,
    generate_frontmatter,
    parse_frontmatter,
)
from entity_store.models import Entity, EntityState, EntityType
from entity_store.neon_client import NeonClient


class EntityRegistry:
    """
    Central registry for entity CRUD operations.

    Coordinates between AST parsers and Neon PostgreSQL storage.
    Provides in-memory entity storage with frontmatter-based persistence.
    """

    def __init__(self, client: NeonClient) -> None:
        """Initialize registry with Neon client."""
        self.client = client
        self._parser_cache: dict[str, object] = {}
        self._entities: dict[str, Entity] = {}
        self._locks: dict[str, dict[str, str | datetime]] = {}

    def parse_file(self, filepath: Path) -> list[Entity]:
        """
        Parse a file and extract entities.

        Args:
            filepath: Path to the file to parse

        Returns:
            List of Entity objects extracted from the file
        """
        from entity_store.parsers.python_parser import PythonParser

        # Determine parser based on file extension
        ext = filepath.suffix.lower()

        if ext == ".py":
            parser = PythonParser()
            return parser.parse_file(filepath)
        else:
            # For now, only Python is supported
            return []

    def register(self, entity: Entity) -> UUID:
        """
        Register a new entity in the store.

        Args:
            entity: Entity to register

        Returns:
            UUID of the registered entity
        """
        entity_id = str(entity.entity_id)
        self._entities[entity_id] = entity
        return entity.entity_id

    def get(self, entity_id: UUID) -> Entity | None:
        """
        Get an entity by ID.

        Args:
            entity_id: UUID of the entity

        Returns:
            Entity if found, None otherwise
        """
        entity_id_str = str(entity_id)
        return self._entities.get(entity_id_str)

    def filter(
        self,
        type_id: EntityType | None = None,
        name_pattern: str | None = None,
        path_pattern: str | None = None,
        state: EntityState = EntityState.ACTIVE,
    ) -> list[Entity]:
        """
        Filter entities by criteria.

        Args:
            type_id: Filter by entity type
            name_pattern: Filter by name pattern (glob)
            path_pattern: Filter by path pattern (glob)
            state: Filter by state (default: active)

        Returns:
            List of matching entities
        """
        import fnmatch

        results = []
        for entity in self._entities.values():
            # Filter by state
            if entity.entity_state != state:
                continue

            # Filter by type
            if type_id is not None and entity.entity_type_id != type_id:
                continue

            # Filter by name pattern
            if name_pattern and not fnmatch.fnmatch(entity.entity_name, name_pattern):
                continue

            # Filter by path pattern
            if path_pattern and not fnmatch.fnmatch(entity.entity_path, path_pattern):
                continue

            results.append(entity)

        return results

    def update(self, entity_id: UUID, **fields) -> Entity:
        """
        Update entity fields.

        Args:
            entity_id: UUID of the entity to update
            **fields: Fields to update

        Returns:
            Updated entity
        """
        entity_id_str = str(entity_id)
        if entity_id_str not in self._entities:
            raise KeyError(f"Entity not found: {entity_id}")

        entity = self._entities[entity_id_str]

        # Update fields
        entity_data = entity.model_dump()
        for key, value in fields.items():
            if key in entity_data:
                entity_data[key] = value

        # Update last_updated timestamp
        entity_data["entity_last_updated"] = datetime.now(UTC)

        # Create updated entity
        updated_entity = Entity(**entity_data)
        self._entities[entity_id_str] = updated_entity

        return updated_entity

    def archive(self, entity_id: UUID) -> None:
        """
        Archive an entity (soft delete).

        Args:
            entity_id: UUID of the entity to archive
        """
        self.update(entity_id, entity_state=EntityState.ARCHIVED)

    def delete(self, entity_id: UUID) -> None:
        """
        Permanently delete an entity.

        Args:
            entity_id: UUID of the entity to delete
        """
        entity_id_str = str(entity_id)
        if entity_id_str in self._entities:
            del self._entities[entity_id_str]
        if entity_id_str in self._locks:
            del self._locks[entity_id_str]

    # === New CRUD methods for in-memory entity store ===

    def lock_entity(self, entity_id: str, locked_by: str) -> bool:
        """
        Lock an entity for editing.

        Sets the entity's locked_by and locked_at fields to prevent
        concurrent modifications by multiple agents.

        Args:
            entity_id: String ID of the entity to lock
            locked_by: Identifier of the agent/user locking the entity

        Returns:
            True if locked successfully, False if already locked
        """
        if entity_id in self._locks:
            # Entity is already locked
            return False

        self._locks[entity_id] = {
            "locked_by": locked_by,
            "locked_at": datetime.now(UTC),
        }
        return True

    def unlock_entity(self, entity_id: str) -> bool:
        """
        Unlock an entity after editing.

        Clears the entity's locked_by and locked_at fields to allow
        other agents to edit.

        Args:
            entity_id: String ID of the entity to unlock

        Returns:
            True if unlocked successfully, False if not locked
        """
        if entity_id not in self._locks:
            return False

        del self._locks[entity_id]
        return True

    def get_entity_dependencies(self, entity_id: str) -> list[str]:
        """
        Get the dependencies of an entity.

        Returns the list of entity_ids that this entity depends on,
        as specified in the entity_dependencies field from frontmatter.

        Args:
            entity_id: String ID of the entity

        Returns:
            List of entity_ids that this entity depends on.
            Empty list if entity not found or has no dependencies.
        """
        entity = self._entities.get(entity_id)
        if entity is None:
            return []

        # Check if entity has metadata with dependencies
        metadata = entity.entity_metadata
        if metadata and "entity_dependencies" in metadata:
            return list(metadata["entity_dependencies"])

        # Try to read dependencies from the file's frontmatter
        if entity.entity_path:
            path = Path(entity.entity_path)
            if path.exists():
                try:
                    content = path.read_text(encoding="utf-8")
                    frontmatter = parse_frontmatter(content, entity.entity_language)
                    if frontmatter:
                        return list(frontmatter.entity_dependencies)
                except Exception:
                    pass

        return []

    def create_entity(self, entity: Entity) -> Entity:
        """
        Add a new entity to the registry.

        Stores the entity in the in-memory registry and optionally
        writes frontmatter to the entity's file if it has a path.

        Args:
            entity: Entity object to add

        Returns:
            The created entity
        """
        entity_id = str(entity.entity_id)
        self._entities[entity_id] = entity

        # Write frontmatter to file if entity has a path
        if entity.entity_path:
            path = Path(entity.entity_path)
            if path.exists():
                try:
                    content = path.read_text(encoding="utf-8")
                    # Check if file already has frontmatter
                    existing_frontmatter = parse_frontmatter(content, entity.entity_language)
                    if existing_frontmatter is None:
                        # Generate and prepend frontmatter
                        # Map EntityType to EntityTypeId
                        type_id_map = {
                            EntityType.CLASS: EntityTypeId.CLASS,
                            EntityType.METHOD: EntityTypeId.METHOD,
                            EntityType.FUNCTION: EntityTypeId.FUNCTION,
                            EntityType.PARAM: EntityTypeId.PARAM,
                            EntityType.HEADING: EntityTypeId.HEADING,
                            EntityType.CODE_BLOCK: EntityTypeId.CODE_BLOCK,
                            EntityType.DOCUMENT: EntityTypeId.DOCUMENT,
                            EntityType.CONFIG: EntityTypeId.CONFIG,
                            EntityType.MODULE: EntityTypeId.MODULE,
                            EntityType.SCHEMA: EntityTypeId.SCHEMA,
                        }
                        entity_type_id = type_id_map.get(entity.entity_type_id, EntityTypeId.MODULE)

                        exports = entity.entity_metadata.get("entity_exports", [])
                        deps = entity.entity_metadata.get("entity_dependencies", [])
                        frontmatter_block = generate_frontmatter(
                            entity_id=entity_id,
                            entity_name=entity.entity_name,
                            entity_type_id=entity_type_id,
                            entity_path=entity.entity_path,
                            language=entity.entity_language,
                            entity_exports=exports,
                            entity_dependencies=deps,
                        )
                        new_content = frontmatter_block + "\n\n" + content
                        path.write_text(new_content, encoding="utf-8")
                except Exception:
                    # Silently ignore file write errors
                    pass

        return entity

    def update_entity(self, entity_id: str, updates: dict) -> Entity:
        """
        Update fields of an existing entity.

        Updates the entity in the registry and updates frontmatter
        in the file if applicable.

        Args:
            entity_id: String ID of the entity to update
            updates: Dictionary of field names to new values

        Returns:
            The updated entity

        Raises:
            KeyError: If entity_id is not found in the registry
        """
        if entity_id not in self._entities:
            raise KeyError(f"Entity not found: {entity_id}")

        entity = self._entities[entity_id]

        # Update entity fields
        entity_data = entity.model_dump()
        for key, value in updates.items():
            if key in entity_data:
                entity_data[key] = value

        # Update last_updated timestamp
        entity_data["entity_last_updated"] = datetime.now(UTC)

        # Create updated entity
        updated_entity = Entity(**entity_data)
        self._entities[entity_id] = updated_entity

        # Update frontmatter in file if entity has a path
        if updated_entity.entity_path:
            path = Path(updated_entity.entity_path)
            if path.exists():
                try:
                    content = path.read_text(encoding="utf-8")
                    frontmatter = parse_frontmatter(content, updated_entity.entity_language)
                    if frontmatter:
                        # Update frontmatter fields
                        frontmatter_data = frontmatter.model_dump()
                        for key, value in updates.items():
                            if key in frontmatter_data:
                                frontmatter_data[key] = value
                        last_updated = datetime.now(UTC).isoformat()
                        frontmatter_data["entity_last_updated"] = last_updated

                        # Regenerate frontmatter and replace in file
                        updated_frontmatter = EntityFrontmatter(**frontmatter_data)
                        yaml_content = updated_frontmatter.to_yaml()

                        # Rebuild frontmatter block based on language
                        language = updated_entity.entity_language
                        if language == "python":
                            lines = ["# ---"]
                            for line in yaml_content.strip().split("\n"):
                                lines.append(f"# {line}")
                            lines.append("# ---")
                            new_frontmatter_block = "\n".join(lines)
                        elif language in ("typescript", "javascript"):
                            lines = ["// ---"]
                            for line in yaml_content.strip().split("\n"):
                                lines.append(f"// {line}")
                            lines.append("// ---")
                            new_frontmatter_block = "\n".join(lines)
                        else:
                            new_frontmatter_block = f"---\n{yaml_content}---"

                        # Replace old frontmatter with new
                        from entity_store.frontmatter import (
                            PYTHON_FRONTMATTER_PATTERN,
                            TS_FRONTMATTER_PATTERN,
                            YAML_FRONTMATTER_PATTERN,
                        )

                        if language == "python":
                            new_content = PYTHON_FRONTMATTER_PATTERN.sub(
                                new_frontmatter_block + "\n", content
                            )
                        elif language in ("typescript", "javascript"):
                            new_content = TS_FRONTMATTER_PATTERN.sub(
                                new_frontmatter_block + "\n", content
                            )
                        else:
                            new_content = YAML_FRONTMATTER_PATTERN.sub(
                                new_frontmatter_block + "\n", content
                            )

                        path.write_text(new_content, encoding="utf-8")
                except Exception:
                    # Silently ignore file update errors
                    pass

        return updated_entity

    def delete_entity(self, entity_id: str) -> bool:
        """
        Remove an entity from the registry.

        Removes the entity from the in-memory store. Does not delete
        the actual file or remove frontmatter from files.

        Args:
            entity_id: String ID of the entity to delete

        Returns:
            True if deleted, False if not found
        """
        if entity_id not in self._entities:
            return False

        del self._entities[entity_id]

        # Also remove any lock on this entity
        if entity_id in self._locks:
            del self._locks[entity_id]

        return True
