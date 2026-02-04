# ---
# entity_id: module-cli
# entity_name: Entity Store CLI
# entity_type_id: module
# entity_path: entity_store/cli.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: [cli, build_index, query, search]
# entity_dependencies: [registry, neon_client, query]
# ---

"""
CLI for entity store operations.

Provides commands for:
- Building/rebuilding the entity index
- Querying entities
- Searching entities
- Cache management
"""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """Entity Store CLI - AST-based entity indexing."""
    pass


@cli.command()
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True, path_type=Path),
    default=".",
    help="Repository path to index",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force reindex even if cache is fresh",
)
def build_index(path: Path, force: bool) -> None:
    """Build or rebuild the entity index."""
    raise NotImplementedError("build_index not yet implemented")


@cli.command()
@click.option("--type-id", "-t", help="Filter by entity type")
@click.option("--name", "-n", help="Filter by name pattern")
@click.option("--path", "-p", help="Filter by path pattern")
@click.option(
    "--fields",
    "-f",
    help="Comma-separated list of fields to return",
)
@click.option("--limit", "-l", type=int, default=100, help="Max results")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def query(
    type_id: str | None,
    name: str | None,
    path: str | None,
    fields: str | None,
    limit: int,
    as_json: bool,
) -> None:
    """Query entities with filters."""
    raise NotImplementedError("query not yet implemented")


@cli.command()
@click.argument("query_text")
@click.option("--limit", "-l", type=int, default=20, help="Max results")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def search(query_text: str, limit: int, as_json: bool) -> None:
    """Full-text search across entities."""
    raise NotImplementedError("search not yet implemented")


@cli.group()
def cache() -> None:
    """Cache management commands."""
    pass


@cache.command()
def clear() -> None:
    """Clear all caches."""
    raise NotImplementedError("cache clear not yet implemented")


@cache.command()
def stats() -> None:
    """Show cache statistics."""
    raise NotImplementedError("cache stats not yet implemented")


@cli.command()
@click.argument("entity_id")
def show(entity_id: str) -> None:
    """Show detailed entity information."""
    raise NotImplementedError("show not yet implemented")


@cli.command()
def store_stats() -> None:
    """Show entity store statistics."""
    raise NotImplementedError("store_stats not yet implemented")


def _display_table(entities: list[dict], fields: list[str]) -> None:
    """Display entities as a Rich table."""
    table = Table(show_header=True, header_style="bold cyan")

    for field in fields:
        table.add_column(field)

    for entity in entities:
        row = [str(entity.get(f, "")) for f in fields]
        table.add_row(*row)

    console.print(table)


if __name__ == "__main__":
    cli()
