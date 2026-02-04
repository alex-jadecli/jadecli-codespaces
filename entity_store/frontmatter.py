# ---
# entity_id: module-frontmatter
# entity_name: Enhanced Frontmatter Schema
# entity_type_id: module
# entity_path: entity_store/frontmatter.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T17:00:00Z
# entity_exports: [EntityFrontmatter, parse_frontmatter, generate_frontmatter]
# entity_dependencies: [pydantic, models]
# entity_callers: [parsers, registry, cli]
# entity_callees: [models]
# entity_semver_impact: major
# entity_breaking_change_risk: high
# ---

"""
Enhanced Frontmatter Schema for AST/Tree-sitter Indexing.

This module defines the comprehensive frontmatter schema that enables:
- Full dependency graph construction
- Breaking change detection
- Sequence diagram generation
- Architecture tree visualization
- Token-efficient Claude navigation

Every code entity (file, class, function, etc.) should have frontmatter
that describes its relationships, enabling fast traversal without
reading full file contents.

Schema Fields:
--------------
Core Identity:
  - entity_id: Unique identifier
  - entity_name: Human-readable name
  - entity_type_id: class|function|method|module|config|schema

Location:
  - entity_path: Relative file path
  - entity_line_start: Start line (1-indexed)
  - entity_line_end: End line (optional)
  - entity_language: python|typescript|sql|markdown

State:
  - entity_state: active|deprecated|archived
  - entity_created: ISO-8601 timestamp
  - entity_last_updated: ISO-8601 timestamp

Dependencies (for graph construction):
  - entity_imports: Modules/packages this entity imports
  - entity_exports: Symbols this entity exports
  - entity_dependencies: Other entities this depends on (by entity_id)

Call Graph (for sequence diagrams):
  - entity_callers: Entities that call this (incoming edges)
  - entity_callees: Entities this calls (outgoing edges)

Versioning (for semver/breaking change detection):
  - entity_semver_impact: major|minor|patch
  - entity_breaking_change_risk: high|medium|low
  - entity_public_api: Is this part of public API?

Actors (for sequence diagrams):
  - entity_actors: [dev, claude, user, coderabbit]
"""

import re
from datetime import datetime
from enum import Enum
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field


class EntityTypeId(str, Enum):
    """Valid entity type identifiers."""

    MODULE = "module"
    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    PARAM = "param"
    HEADING = "heading"
    CODE_BLOCK = "code_block"
    DOCUMENT = "document"
    CONFIG = "config"
    SCHEMA = "schema"
    HOOK = "hook"
    COMMAND = "command"
    RULE = "rule"


class SemverImpact(str, Enum):
    """Semantic versioning impact levels."""

    MAJOR = "major"  # Breaking change
    MINOR = "minor"  # New feature, backwards compatible
    PATCH = "patch"  # Bug fix, no API change


class BreakingChangeRisk(str, Enum):
    """Risk level for breaking changes."""

    HIGH = "high"  # Many dependents, public API
    MEDIUM = "medium"  # Some dependents, internal API
    LOW = "low"  # Few/no dependents, private


class Actor(str, Enum):
    """Actors for sequence diagrams."""

    DEV = "dev"  # Developer
    CLAUDE = "claude"  # Claude Code
    USER = "user"  # End user
    CODERABBIT = "coderabbit"  # CodeRabbit CLI


class EntityFrontmatter(BaseModel):
    """
    Complete frontmatter schema for AST-indexed entities.

    This schema captures all metadata needed for:
    - Dependency graph construction
    - Breaking change detection
    - Sequence diagram generation
    - Architecture visualization
    """

    model_config = ConfigDict(
        extra="allow",  # Allow custom fields
        str_strip_whitespace=True,
    )

    # === Core Identity ===
    entity_id: str = Field(
        ...,
        description="Unique identifier (format: type-name or uuid)",
    )
    entity_name: str = Field(
        ...,
        min_length=1,
        description="Human-readable name",
    )
    entity_type_id: EntityTypeId = Field(
        ...,
        description="Type of entity",
    )

    # === Location ===
    entity_path: str = Field(
        ...,
        description="Relative file path",
    )
    entity_line_start: int | None = Field(
        default=None,
        ge=1,
        description="Start line number (1-indexed)",
    )
    entity_line_end: int | None = Field(
        default=None,
        ge=1,
        description="End line number",
    )
    entity_language: str = Field(
        default="python",
        description="Programming language",
    )

    # === State ===
    entity_state: Literal["active", "deprecated", "archived"] = Field(
        default="active",
        description="Lifecycle state",
    )
    entity_created: str = Field(
        ...,
        description="Creation timestamp (ISO-8601)",
    )
    entity_last_updated: str | None = Field(
        default=None,
        description="Last update timestamp (ISO-8601)",
    )

    # === Dependencies (Graph Construction) ===
    entity_imports: list[str] = Field(
        default_factory=list,
        description="Modules/packages this entity imports",
    )
    entity_exports: list[str] = Field(
        default_factory=list,
        description="Symbols this entity exports",
    )
    entity_dependencies: list[str] = Field(
        default_factory=list,
        description="Other entity_ids this depends on",
    )

    # === Call Graph (Sequence Diagrams) ===
    entity_callers: list[str] = Field(
        default_factory=list,
        description="Entity IDs that call this (incoming edges)",
    )
    entity_callees: list[str] = Field(
        default_factory=list,
        description="Entity IDs this calls (outgoing edges)",
    )

    # === Versioning (Breaking Change Detection) ===
    entity_semver_impact: SemverImpact = Field(
        default=SemverImpact.PATCH,
        description="Semantic versioning impact if changed",
    )
    entity_breaking_change_risk: BreakingChangeRisk = Field(
        default=BreakingChangeRisk.LOW,
        description="Risk level for breaking changes",
    )
    entity_public_api: bool = Field(
        default=False,
        description="Is this part of the public API?",
    )

    # === Actors (Sequence Diagrams) ===
    entity_actors: list[Actor] = Field(
        default_factory=list,
        description="Actors involved with this entity",
    )

    # === Documentation ===
    entity_docstring: str | None = Field(
        default=None,
        description="Brief description or docstring",
    )
    entity_signature: str | None = Field(
        default=None,
        description="Function/method signature",
    )

    def get_upstream_dependencies(self) -> list[str]:
        """Get all entities this depends on (upstream)."""
        return list(set(self.entity_dependencies + self.entity_callees))

    def get_downstream_dependents(self) -> list[str]:
        """Get all entities that depend on this (downstream)."""
        return list(set(self.entity_callers))

    def would_break_dependents(self) -> bool:
        """Check if modifying this would break dependents."""
        return (
            self.entity_breaking_change_risk == BreakingChangeRisk.HIGH
            or self.entity_public_api
            or len(self.entity_callers) > 3
        )

    def to_yaml(self) -> str:
        """Serialize to YAML frontmatter block."""
        data = self.model_dump(
            exclude_none=True,
            exclude_defaults=True,
        )
        # Convert enums to strings
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.value
            elif isinstance(value, list):
                data[key] = [v.value if isinstance(v, Enum) else v for v in value]

        return yaml.dump(data, default_flow_style=False, sort_keys=False)


# === Parsing Functions ===

PYTHON_FRONTMATTER_PATTERN = re.compile(r"^# ---\s*\n((?:# .*\n)+)# ---\s*\n", re.MULTILINE)

YAML_FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

TS_FRONTMATTER_PATTERN = re.compile(r"^// ---\s*\n((?:// .*\n)+)// ---\s*\n", re.MULTILINE)


def parse_frontmatter(source: str, language: str = "python") -> EntityFrontmatter | None:
    """
    Parse frontmatter from source code.

    Args:
        source: Source code content
        language: Programming language (python, typescript, markdown)

    Returns:
        EntityFrontmatter if found, None otherwise
    """
    if language == "python":
        match = PYTHON_FRONTMATTER_PATTERN.match(source)
        if match:
            # Remove '# ' prefix from each line
            yaml_content = "\n".join(
                line[2:] if line.startswith("# ") else line for line in match.group(1).split("\n")
            )
    elif language in ("typescript", "javascript"):
        match = TS_FRONTMATTER_PATTERN.match(source)
        if match:
            # Remove '// ' prefix from each line
            yaml_content = "\n".join(
                line[3:] if line.startswith("// ") else line for line in match.group(1).split("\n")
            )
    elif language == "markdown":
        match = YAML_FRONTMATTER_PATTERN.match(source)
        if match:
            yaml_content = match.group(1)
    else:
        return None

    if not match:
        return None

    try:
        data = yaml.safe_load(yaml_content)
        if data:
            return EntityFrontmatter(**data)
    except Exception:
        pass

    return None


def generate_frontmatter(
    entity_id: str,
    entity_name: str,
    entity_type_id: EntityTypeId,
    entity_path: str,
    language: str = "python",
    **kwargs,
) -> str:
    """
    Generate frontmatter block for a new entity.

    Args:
        entity_id: Unique identifier
        entity_name: Human-readable name
        entity_type_id: Type of entity
        entity_path: Relative file path
        language: Programming language
        **kwargs: Additional frontmatter fields

    Returns:
        Formatted frontmatter block
    """
    frontmatter = EntityFrontmatter(
        entity_id=entity_id,
        entity_name=entity_name,
        entity_type_id=entity_type_id,
        entity_path=entity_path,
        entity_language=language,
        entity_created=datetime.utcnow().isoformat() + "Z",
        **kwargs,
    )

    yaml_content = frontmatter.to_yaml()

    if language == "python":
        lines = ["# ---"]
        for line in yaml_content.strip().split("\n"):
            lines.append(f"# {line}")
        lines.append("# ---")
        return "\n".join(lines)

    elif language in ("typescript", "javascript"):
        lines = ["// ---"]
        for line in yaml_content.strip().split("\n"):
            lines.append(f"// {line}")
        lines.append("// ---")
        return "\n".join(lines)

    elif language == "markdown":
        return f"---\n{yaml_content}---"

    else:
        return f"---\n{yaml_content}---"
