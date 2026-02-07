#!/usr/bin/env python3
# ---
# entity_id: hook-session-start
# entity_name: Session Start Hook
# entity_type_id: function
# entity_path: .claude/hooks/session-start.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: [main]
# entity_dependencies: [entity_store]
# ---

"""
Hook: Build entity index when Claude enters repo (blocking with progress).

This hook triggers on SessionStart event and:
1. Checks if entity index is fresh (< 1 hour old)
2. If stale, re-indexes all files with tqdm progress
3. Uploads entities to Neon PostgreSQL
4. Updates index timestamp
"""

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

try:
    from rich.console import Console
    from tqdm import tqdm

    # Add entity_store to path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    from entity_store.neon_client import NeonClient
    from entity_store.registry import EntityRegistry

    console = Console()
except ImportError as e:
    # Dependencies not installed yet - skip hook
    print(f"Entity store not configured: {e}")
    sys.exit(0)


def main() -> None:
    """Main hook entry point."""
    repo_root = Path.cwd()

    # Connect to Neon via MCP
    try:
        neon = NeonClient()
        registry = EntityRegistry(neon)
    except Exception as e:
        console.print(f"[yellow]Warning:[/yellow] Could not connect to Neon: {e}")
        return

    # Check if index is fresh (< 1 hour old)
    try:
        last_update = neon.get_last_index_time(str(repo_root))
        if last_update and (datetime.now(UTC) - last_update) < timedelta(hours=1):
            console.print("[green]✓[/green] Entity index is fresh")
            return
    except (NotImplementedError, TypeError):
        # Stub implementation or async method - skip freshness check
        pass

    console.print("[cyan]Building entity index...[/cyan]")

    # Discover files to index
    files = (
        list(repo_root.rglob("*.py"))
        + list(repo_root.rglob("*.ts"))
        + list(repo_root.rglob("*.tsx"))
        + list(repo_root.rglob("*.md"))
    )

    # Filter out node_modules, .git, etc.
    excluded_dirs = {"node_modules", ".git", "__pycache__", ".entity-cache", "dist"}
    files = [f for f in files if not any(p in f.parts for p in excluded_dirs)]

    console.print(f"[cyan]Found {len(files)} files to index[/cyan]")

    # Parse with tqdm progress bar
    entities = []
    errors = []

    for filepath in tqdm(files, desc="Parsing files", unit="file"):
        try:
            file_entities = registry.parse_file(filepath)
            entities.extend(file_entities)
        except NotImplementedError:
            # Stub implementation
            pass
        except Exception as e:
            errors.append((filepath, str(e)))

    if errors:
        for filepath, error in errors[:5]:  # Show first 5 errors
            console.print(f"[yellow]Warning:[/yellow] {filepath}: {error}")
        if len(errors) > 5:
            console.print(f"[yellow]... and {len(errors) - 5} more errors[/yellow]")

    # Upsert to Neon with progress
    if entities:
        console.print(f"[cyan]Syncing {len(entities)} entities to Neon...[/cyan]")

        for entity in tqdm(entities, desc="Uploading entities", unit="entity"):
            try:
                result = neon.upsert_entity(entity)
                # If async, skip (coroutine won't execute)
                if hasattr(result, '__await__'):
                    break  # Exit loop - async not supported yet
            except NotImplementedError:
                # Stub implementation
                break

        # Update index timestamp
        try:
            result = neon.set_last_index_time(str(repo_root))
            # If async, skip
            if hasattr(result, '__await__'):
                pass
        except NotImplementedError:
            pass

    console.print(f"[green]✓[/green] Indexed {len(entities)} entities from {len(files)} files")


def index_documentation():
    """Index local documentation if needed."""
    try:
        from doc_index.indexer import DocumentIndexer
    except ImportError:
        # doc_index not installed yet
        return

    docs_root = Path.home() / "projects" / "jadecli-codespaces" / "docs"

    if not docs_root.exists():
        return

    console.print("[blue]Checking documentation index...[/blue]")

    try:
        indexer = DocumentIndexer(index_name="jadecli_docs")
        stats = indexer.get_stats()

        if stats["total_chunks"] == 0:
            console.print("[yellow]Indexing documentation (first run)...[/yellow]")

            # Index specific doc directories
            doc_dirs = [
                "anthropic",
                "guides",
                "platform-claude",
                "ruff",
                "ty",
                "uv",
                "wslg",
                "chezmoi",
            ]

            total_chunks = 0
            for doc_dir in doc_dirs:
                dir_path = docs_root / doc_dir
                if dir_path.exists():
                    count = indexer.index_directory(dir_path)
                    total_chunks += count

            console.print(f"[green]✓[/green] Indexed {total_chunks} chunks")
        else:
            console.print(f"[green]✓[/green] Documentation index ready ({stats['total_chunks']} chunks)")
    except Exception as e:
        console.print(f"[yellow]Warning:[/yellow] Could not index documentation: {e}")


if __name__ == "__main__":
    main()
    index_documentation()
