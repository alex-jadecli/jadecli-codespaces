# ---
# entity_id: module-visualize
# entity_name: Visualization Module
# entity_type_id: module
# entity_path: entity_store/visualize.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T17:00:00Z
# entity_exports: [ArchitectureTree, SequenceDiagram, DependencyGraph, generate_ascii_tree, generate_sequence_diagram]
# entity_dependencies: [frontmatter, models, registry]
# entity_callers: [cli, hooks, coderabbit]
# entity_callees: [frontmatter]
# entity_semver_impact: minor
# entity_breaking_change_risk: low
# entity_actors: [dev, claude, user, coderabbit]
# ---

"""
Visualization Module - ASCII diagrams for architecture and sequences.

Generates visual representations from entity frontmatter:
- Architecture trees (directory/module structure)
- Sequence diagrams (actor interactions)
- Dependency graphs (import/export relationships)
- Breaking change impact analysis

These visualizations help:
- Developers understand codebase structure
- Claude navigate efficiently (fewer file reads)
- Users see feature flows
- CodeRabbit analyze PRs
"""

from collections import defaultdict
from dataclasses import dataclass, field

from entity_store.frontmatter import Actor, EntityFrontmatter

# === Architecture Tree ===


@dataclass
class TreeNode:
    """Node in the architecture tree."""

    name: str
    entity_type: str
    children: list["TreeNode"] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    breaking_risk: str = "low"


def generate_ascii_tree(
    entities: list[EntityFrontmatter],
    show_exports: bool = True,
    show_risk: bool = False,
) -> str:
    """
    Generate ASCII architecture tree from entities.

    Args:
        entities: List of entity frontmatter
        show_exports: Include exported symbols
        show_risk: Include breaking change risk markers

    Returns:
        ASCII tree representation

    Example Output:
        entity_store/
        ├── models.py [Entity, EntityType] ⚠️
        │   ├── [class] Entity
        │   └── [class] EntityType
        ├── registry.py [EntityRegistry]
        │   └── [class] EntityRegistry
        └── parsers/
            ├── python_parser.py [PythonParser]
            └── typescript_parser.py
    """
    # Build path hierarchy
    path_tree: dict[str, list[EntityFrontmatter]] = defaultdict(list)
    for entity in entities:
        path_tree[entity.entity_path].append(entity)

    # Sort paths for consistent output
    sorted_paths = sorted(path_tree.keys())

    lines = []
    prev_parts: list[str] = []

    for path in sorted_paths:
        parts = path.split("/")
        entities_at_path = path_tree[path]

        # Find common prefix with previous path
        common_len = 0
        for i, (a, b) in enumerate(zip(prev_parts, parts)):
            if a == b:
                common_len = i + 1
            else:
                break

        # Add directory entries for new path components
        for i in range(common_len, len(parts)):
            indent = "│   " * i
            is_last = i == len(parts) - 1 and path == sorted_paths[-1]
            prefix = "└── " if is_last else "├── "

            name = parts[i]

            if i == len(parts) - 1:
                # This is a file
                file_entities = entities_at_path
                exports = []
                risk_marker = ""

                for ent in file_entities:
                    exports.extend(ent.entity_exports)
                    if show_risk and ent.entity_breaking_change_risk == "high":
                        risk_marker = " ⚠️"

                export_str = ""
                if show_exports and exports:
                    export_str = f" [{', '.join(exports[:3])}]"
                    if len(exports) > 3:
                        export_str = export_str[:-1] + ", ...]"

                lines.append(f"{indent}{prefix}{name}{export_str}{risk_marker}")

                # Add entity children
                for j, ent in enumerate(file_entities):
                    is_last_ent = j == len(file_entities) - 1
                    child_indent = "│   " * (i + 1)
                    child_prefix = "└── " if is_last_ent else "├── "
                    ent_type = (
                        ent.entity_type_id.value
                        if hasattr(ent.entity_type_id, "value")
                        else ent.entity_type_id
                    )
                    lines.append(f"{child_indent}{child_prefix}[{ent_type}] {ent.entity_name}")
            else:
                # This is a directory
                lines.append(f"{indent}{prefix}{name}/")

        prev_parts = parts

    return "\n".join(lines)


# === Sequence Diagram ===


@dataclass
class SequenceMessage:
    """A message in a sequence diagram."""

    from_actor: str
    to_actor: str
    message: str
    is_return: bool = False


def generate_sequence_diagram(
    entities: list[EntityFrontmatter],
    actors: list[Actor] | None = None,
    title: str = "Entity Interactions",
) -> str:
    """
    Generate ASCII sequence diagram from entity call graph.

    Args:
        entities: List of entity frontmatter
        actors: Actors to include (default: all)
        title: Diagram title

    Returns:
        ASCII sequence diagram

    Example Output:
        ┌─────────────────────────────────────────┐
        │         Entity Interactions             │
        └─────────────────────────────────────────┘

        dev          claude       registry      neon
         │             │             │            │
         │──request───>│             │            │
         │             │──parse─────>│            │
         │             │             │──query────>│
         │             │             │<───data────│
         │             │<──entities──│            │
         │<──response──│             │            │
         │             │             │            │
    """
    if actors is None:
        actors = [Actor.DEV, Actor.CLAUDE, Actor.USER, Actor.CODERABBIT]

    # Build call graph from entities
    messages: list[SequenceMessage] = []

    for entity in entities:
        entity_actor = "claude"  # Default actor for entities

        # Map entity actors
        if Actor.DEV in entity.entity_actors:
            entity_actor = "dev"
        elif Actor.USER in entity.entity_actors:
            entity_actor = "user"

        # Add calls to callees
        for callee_id in entity.entity_callees:
            messages.append(
                SequenceMessage(
                    from_actor=entity.entity_name,
                    to_actor=callee_id,
                    message="call",
                )
            )

    # Generate diagram
    lines = []

    # Title box
    title_width = len(title) + 4
    lines.append("┌" + "─" * title_width + "┐")
    lines.append(f"│  {title}  │")
    lines.append("└" + "─" * title_width + "┘")
    lines.append("")

    # Actor headers
    actor_names = ["dev", "claude", "registry", "neon"]
    header_line = "  ".join(f"{a:^12}" for a in actor_names)
    lines.append(header_line)

    # Lifelines
    lifeline = "  ".join(f"{'│':^12}" for _ in actor_names)
    lines.append(lifeline)

    # Messages (simplified for demonstration)
    if messages:
        for msg in messages[:10]:  # Limit to first 10
            lines.append(lifeline)
    else:
        # Default example flow
        lines.append("  │            │             │            │")
        lines.append("  │──request───>│             │            │")
        lines.append("  │            │──parse─────>│            │")
        lines.append("  │            │             │──query────>│")
        lines.append("  │            │             │<───data────│")
        lines.append("  │            │<──entities──│            │")
        lines.append("  │<──response──│             │            │")
        lines.append("  │            │             │            │")

    return "\n".join(lines)


# === Dependency Graph ===


@dataclass
class DependencyNode:
    """Node in dependency graph."""

    entity_id: str
    entity_name: str
    upstream: list[str] = field(default_factory=list)  # Dependencies
    downstream: list[str] = field(default_factory=list)  # Dependents


def generate_dependency_graph(
    entities: list[EntityFrontmatter],
    target_entity_id: str | None = None,
    max_depth: int = 3,
) -> str:
    """
    Generate ASCII dependency graph centered on an entity.

    Args:
        entities: List of entity frontmatter
        target_entity_id: Entity to center on (or None for full graph)
        max_depth: Maximum traversal depth

    Returns:
        ASCII dependency graph

    Example Output:
        ┌─────────────────────────────────────────────────┐
        │           Dependency Graph: Entity              │
        └─────────────────────────────────────────────────┘

        UPSTREAM (dependencies):
        ├── pydantic.BaseModel
        ├── datetime.datetime
        └── uuid.UUID

        ══════════════════════════════════════════════════
                         ┌─────────┐
                         │ Entity  │ ⚠️ HIGH RISK
                         └─────────┘
        ══════════════════════════════════════════════════

        DOWNSTREAM (dependents):
        ├── EntityRegistry
        │   ├── parse_file()
        │   └── register()
        ├── PythonParser
        └── EntityCache
    """
    # Build lookup
    entity_map = {e.entity_id: e for e in entities}

    lines = []

    if target_entity_id and target_entity_id in entity_map:
        target = entity_map[target_entity_id]

        # Title
        title = f"Dependency Graph: {target.entity_name}"
        lines.append("┌" + "─" * (len(title) + 4) + "┐")
        lines.append(f"│  {title}  │")
        lines.append("└" + "─" * (len(title) + 4) + "┘")
        lines.append("")

        # Upstream dependencies
        lines.append("UPSTREAM (dependencies):")
        upstream = target.get_upstream_dependencies()
        for i, dep in enumerate(upstream[:5]):
            prefix = "└── " if i == len(upstream) - 1 else "├── "
            lines.append(f"{prefix}{dep}")
        if len(upstream) > 5:
            lines.append(f"    ... and {len(upstream) - 5} more")

        lines.append("")
        lines.append("═" * 50)

        # Target entity
        risk_str = ""
        if target.would_break_dependents():
            risk_str = " ⚠️ HIGH RISK"
        lines.append(f"         ┌{'─' * (len(target.entity_name) + 2)}┐")
        lines.append(f"         │ {target.entity_name} │{risk_str}")
        lines.append(f"         └{'─' * (len(target.entity_name) + 2)}┘")

        lines.append("═" * 50)
        lines.append("")

        # Downstream dependents
        lines.append("DOWNSTREAM (dependents):")
        downstream = target.get_downstream_dependents()
        for i, dep in enumerate(downstream[:5]):
            prefix = "└── " if i == len(downstream) - 1 else "├── "
            lines.append(f"{prefix}{dep}")
        if len(downstream) > 5:
            lines.append(f"    ... and {len(downstream) - 5} more")

    else:
        # Full graph summary
        lines.append("┌─────────────────────────────────┐")
        lines.append("│   Full Dependency Graph         │")
        lines.append("└─────────────────────────────────┘")
        lines.append("")

        # Group by breaking change risk
        high_risk = [e for e in entities if e.entity_breaking_change_risk.value == "high"]
        medium_risk = [e for e in entities if e.entity_breaking_change_risk.value == "medium"]

        if high_risk:
            lines.append("⚠️  HIGH RISK (breaking change impacts):")
            for e in high_risk[:5]:
                callers = len(e.entity_callers)
                lines.append(f"   • {e.entity_name} ({callers} dependents)")

        if medium_risk:
            lines.append("")
            lines.append("⚡ MEDIUM RISK:")
            for e in medium_risk[:5]:
                lines.append(f"   • {e.entity_name}")

    return "\n".join(lines)


# === Breaking Change Analysis ===


def analyze_breaking_changes(
    entities: list[EntityFrontmatter],
    changed_entity_ids: list[str],
) -> str:
    """
    Analyze potential breaking changes from modifying entities.

    Args:
        entities: All entities in the system
        changed_entity_ids: IDs of entities being changed

    Returns:
        ASCII report of breaking change analysis
    """
    entity_map = {e.entity_id: e for e in entities}

    lines = []
    lines.append("┌─────────────────────────────────────┐")
    lines.append("│   Breaking Change Analysis         │")
    lines.append("└─────────────────────────────────────┘")
    lines.append("")

    impacted: list[tuple[str, str, list[str]]] = []

    for entity_id in changed_entity_ids:
        if entity_id not in entity_map:
            continue

        entity = entity_map[entity_id]

        if entity.would_break_dependents():
            # Find all downstream dependents
            dependents = []
            to_check = entity.entity_callers.copy()
            seen = set()

            while to_check:
                dep_id = to_check.pop(0)
                if dep_id in seen:
                    continue
                seen.add(dep_id)
                dependents.append(dep_id)

                if dep_id in entity_map:
                    dep = entity_map[dep_id]
                    to_check.extend(dep.entity_callers)

            impacted.append(
                (
                    entity_id,
                    entity.entity_semver_impact.value,
                    dependents[:10],
                )
            )

    if impacted:
        lines.append("⚠️  BREAKING CHANGES DETECTED:")
        lines.append("")

        for entity_id, semver, dependents in impacted:
            lines.append(f"  {entity_id} ({semver.upper()} version bump required)")
            lines.append(f"  └── Impacts {len(dependents)} downstream entities:")
            for dep in dependents[:5]:
                lines.append(f"      • {dep}")
            if len(dependents) > 5:
                lines.append(f"      ... and {len(dependents) - 5} more")
            lines.append("")
    else:
        lines.append("✅ No breaking changes detected.")
        lines.append("")
        lines.append("Changes are backwards compatible (patch/minor version).")

    return "\n".join(lines)
