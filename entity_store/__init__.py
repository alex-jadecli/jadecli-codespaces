# ---
# entity_id: module-entity-store
# entity_name: Entity Store Package
# entity_type_id: module
# entity_path: entity_store/__init__.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: [Entity, EntityType, EntityRegistry, EntityCache, EntityFrontmatter]
# entity_dependencies: [models, registry, cache, frontmatter, visualize]
# entity_callers: [cli, hooks, coderabbit]
# entity_callees: []
# entity_semver_impact: major
# entity_breaking_change_risk: high
# entity_public_api: true
# ---

"""
Entity Store - AST-based entity indexing system for multi-agent Claude collaboration.

This package provides:
- Entity models with Pydantic validation
- Enhanced frontmatter schema for dependency tracking
- AST parsers for Python, TypeScript, and Markdown
- Neon PostgreSQL client for persistent storage
- GraphQL-like query interface
- Local caching for token reduction
- Architecture and sequence diagram visualization
- Breaking change detection
"""

from entity_store.cache import EntityCache
from entity_store.frontmatter import EntityFrontmatter, generate_frontmatter, parse_frontmatter
from entity_store.models import Entity, EntityType
from entity_store.registry import EntityRegistry
from entity_store.visualize import (
    analyze_breaking_changes,
    generate_ascii_tree,
    generate_dependency_graph,
    generate_sequence_diagram,
)

__all__ = [
    # Models
    "Entity",
    "EntityType",
    "EntityRegistry",
    "EntityCache",
    # Frontmatter
    "EntityFrontmatter",
    "parse_frontmatter",
    "generate_frontmatter",
    # Visualization
    "generate_ascii_tree",
    "generate_sequence_diagram",
    "generate_dependency_graph",
    "analyze_breaking_changes",
]
__version__ = "0.1.0"
