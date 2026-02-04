# ---
# entity_id: module-models
# entity_name: Entity Models
# entity_type_id: module
# entity_path: entity_store/models.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: [Entity, EntityType, EntityState]
# entity_dependencies: []
# ---

"""
Pydantic models for entity store.

Defines the core Entity model and supporting types used throughout
the entity indexing system.
"""

import hashlib
from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class EntityType(str, Enum):
    """Valid entity type identifiers."""

    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    PARAM = "param"
    HEADING = "heading"
    CODE_BLOCK = "code_block"
    DOCUMENT = "document"
    CONFIG = "config"
    MODULE = "module"
    SCHEMA = "schema"


class EntityState(str, Enum):
    """Entity lifecycle states."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class Entity(BaseModel):
    """
    Core entity model for AST-indexed code elements.

    Every code element (class, function, method, etc.) is represented
    as an Entity with standardized metadata for querying and tracking.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    # Core fields
    entity_id: UUID = Field(default_factory=uuid4)
    entity_name: str = Field(..., min_length=1)
    entity_type_id: EntityType
    entity_frontmatter_signature: str = Field(default="")
    entity_last_updated: datetime = Field(default_factory=lambda: datetime.now(UTC))
    entity_state: EntityState = EntityState.ACTIVE
    entity_created: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Extended fields
    entity_path: str = Field(..., min_length=1)
    entity_line_start: int = Field(ge=1)
    entity_line_end: int | None = Field(default=None, ge=1)
    entity_parent_id: UUID | None = None
    entity_language: str = Field(default="python")
    entity_signature: str | None = None
    entity_docstring: str | None = None
    entity_metadata: dict = Field(default_factory=dict)

    @classmethod
    def compute_signature(cls, path: str, name: str, type_id: str, source: str) -> str:
        """Compute deterministic signature for change detection."""
        content = f"{path}:{name}:{type_id}:{source}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def to_search_text(self) -> str:
        """Generate text for full-text search indexing."""
        parts = [self.entity_name, self.entity_path]
        if self.entity_docstring:
            parts.append(self.entity_docstring)
        return " ".join(parts)
