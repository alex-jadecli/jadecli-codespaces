# ---
# entity_id: module-parsers
# entity_name: AST Parsers Package
# entity_type_id: module
# entity_path: entity_store/parsers/__init__.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: [PythonParser, TypeScriptParser, MarkdownParser, get_parser]
# entity_dependencies: [python_parser, typescript_parser, markdown_parser]
# ---

"""
AST Parsers for entity extraction.

Provides language-specific parsers that extract entities from source files:
- PythonParser: Classes, functions, methods from Python AST
- TypeScriptParser: Classes, functions, interfaces from TS/TSX
- MarkdownParser: Headings, code blocks, frontmatter from Markdown
"""

from pathlib import Path
from typing import Protocol

from entity_store.models import Entity


class Parser(Protocol):
    """Protocol for language-specific parsers."""

    def parse(self, filepath: Path, source: str) -> list[Entity]:
        """Parse source and extract entities."""
        ...


def get_parser(filepath: Path) -> Parser:
    """
    Get the appropriate parser for a file.

    Args:
        filepath: Path to the file

    Returns:
        Parser instance for the file type

    Raises:
        ValueError: If no parser available for file type
    """
    from entity_store.parsers.markdown_parser import MarkdownParser
    from entity_store.parsers.python_parser import PythonParser
    from entity_store.parsers.typescript_parser import TypeScriptParser

    suffix = filepath.suffix.lower()

    if suffix == ".py":
        return PythonParser()
    elif suffix in (".ts", ".tsx", ".js", ".jsx"):
        return TypeScriptParser()
    elif suffix in (".md", ".markdown"):
        return MarkdownParser()
    else:
        raise ValueError(f"No parser available for {suffix} files")


__all__ = ["Parser", "get_parser", "PythonParser", "TypeScriptParser", "MarkdownParser"]
