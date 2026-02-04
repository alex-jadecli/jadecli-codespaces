#!/usr/bin/env python3
# ---
# entity_id: hook-post-tool-use
# entity_name: Post Tool Use Hook
# entity_type_id: function
# entity_path: .claude/hooks/post-tool-use.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: [main]
# entity_dependencies: [entity_store]
# ---

"""
Hook: Invalidate cache after file modifications.

This hook triggers on PostToolUse event for Write/Edit tools and:
1. Detects which files were modified
2. Invalidates related cache entries
3. Re-indexes modified files
4. Logs changes for audit trail
"""

import json
import os
import sys
from pathlib import Path

try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    from entity_store.cache import EntityCache
    from entity_store.neon_client import NeonClient
    from entity_store.registry import EntityRegistry
except ImportError:
    # Dependencies not installed yet - skip hook
    sys.exit(0)


def main() -> None:
    """Main hook entry point."""
    # Read hook input from environment
    tool_name = os.environ.get("CLAUDE_TOOL_NAME", "")
    tool_input = os.environ.get("CLAUDE_TOOL_INPUT", "{}")

    # Only process Write and Edit tools
    if tool_name not in ("Write", "Edit"):
        return

    try:
        input_data = json.loads(tool_input)
    except json.JSONDecodeError:
        return

    # Get the file path that was modified
    file_path = input_data.get("file_path") or input_data.get("path")
    if not file_path:
        return

    file_path = Path(file_path)

    # Skip files outside tracked directories
    tracked_dirs = {"entity_store", "entity_cli", "context", ".claude"}
    if not any(part in file_path.parts for part in tracked_dirs):
        return

    # Initialize cache and registry
    try:
        cache = EntityCache()
        neon = NeonClient()
        registry = EntityRegistry(neon)
    except Exception:
        return

    # Invalidate cache entries for this file
    try:
        cache.invalidate_pattern(f"*{file_path}*")
    except NotImplementedError:
        pass

    # Re-index the modified file
    if file_path.exists():
        try:
            entities = registry.parse_file(file_path)
            for entity in entities:
                try:
                    neon.upsert_entity(entity)
                except NotImplementedError:
                    pass
        except NotImplementedError:
            pass
        except Exception as e:
            print(f"Warning: Could not re-index {file_path}: {e}", file=sys.stderr)

    # Log the change
    try:
        neon.log_change(
            entity_id=None,  # Will be set by the function
            entity_path=str(file_path),
            change_type="update",
            old_signature=None,
            new_signature=None,
        )
    except NotImplementedError:
        pass


if __name__ == "__main__":
    main()
