# ---
# entity_id: module-python-parser
# entity_name: Python AST Parser
# entity_type_id: module
# entity_path: entity_store/parsers/python_parser.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: [PythonParser, PythonEntityExtractor]
# entity_dependencies: [models]
# ---

"""
Python AST parser for entity extraction.

Uses Python's built-in ast module to extract:
- Classes (with docstrings)
- Methods (instance, class, static)
- Functions (module-level)
- Parameters (with type hints)
"""

import ast
from pathlib import Path

from entity_store.models import Entity, EntityType


class PythonEntityExtractor(ast.NodeVisitor):
    """
    AST visitor that extracts entities from Python source.

    Traverses the AST and creates Entity objects for each
    class, method, function, and parameter definition.
    """

    def __init__(self, filepath: str, source: str) -> None:
        """
        Initialize extractor.

        Args:
            filepath: Path to the source file
            source: Source code content
        """
        self.filepath = filepath
        self.source = source
        self.entities: list[Entity] = []
        self.parent_stack: list[Entity] = []

    def extract(self) -> list[Entity]:
        """
        Parse source and extract all entities.

        Returns:
            List of extracted Entity objects
        """
        tree = ast.parse(self.source)
        self.visit(tree)
        return self.entities

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Extract entity from class definition."""
        docstring = ast.get_docstring(node)

        entity = Entity(
            entity_name=node.name,
            entity_type_id=EntityType.CLASS,
            entity_path=self.filepath,
            entity_line_start=node.lineno,
            entity_line_end=node.end_lineno,
            entity_language="python",
            entity_docstring=docstring,
            entity_parent_id=self._get_parent_id(),
        )

        self.entities.append(entity)
        self.parent_stack.append(entity)
        self.generic_visit(node)
        self.parent_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Extract entity from function/method definition."""
        docstring = ast.get_docstring(node)
        signature = self._get_signature(node)

        # Determine if this is a method (inside a class) or a function
        is_method = bool(self.parent_stack)
        entity_type = EntityType.METHOD if is_method else EntityType.FUNCTION

        entity = Entity(
            entity_name=node.name,
            entity_type_id=entity_type,
            entity_path=self.filepath,
            entity_line_start=node.lineno,
            entity_line_end=node.end_lineno,
            entity_language="python",
            entity_signature=signature,
            entity_docstring=docstring,
            entity_parent_id=self._get_parent_id(),
        )

        self.entities.append(entity)
        # Don't traverse into function body (we don't want nested functions for now)
        # self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Extract entity from async function/method definition."""
        docstring = ast.get_docstring(node)
        signature = self._get_signature(node)

        # Determine if this is a method (inside a class) or a function
        is_method = bool(self.parent_stack)
        entity_type = EntityType.METHOD if is_method else EntityType.FUNCTION

        entity = Entity(
            entity_name=node.name,
            entity_type_id=entity_type,
            entity_path=self.filepath,
            entity_line_start=node.lineno,
            entity_line_end=node.end_lineno,
            entity_language="python",
            entity_signature=signature,
            entity_docstring=docstring,
            entity_parent_id=self._get_parent_id(),
        )

        self.entities.append(entity)
        # Don't traverse into function body

    def _get_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Extract function signature string."""
        # Build argument list
        args_parts = []

        # Regular arguments
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args_parts.append(arg_str)

        # Build return type
        returns = ""
        if node.returns:
            returns = f" -> {ast.unparse(node.returns)}"

        # Async prefix
        prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""

        return f"{prefix}def {node.name}({', '.join(args_parts)}){returns}"

    def _get_parent_id(self) -> str | None:
        """Get parent entity ID from stack."""
        if self.parent_stack:
            return self.parent_stack[-1].entity_id
        return None


class PythonParser:
    """
    Parser for Python source files.

    Coordinates AST parsing and entity extraction.
    """

    def parse(self, filepath: Path, source: str) -> list[Entity]:
        """
        Parse Python source and extract entities.

        Args:
            filepath: Path to the source file
            source: Source code content

        Returns:
            List of extracted Entity objects
        """
        extractor = PythonEntityExtractor(str(filepath), source)
        return extractor.extract()

    def parse_file(self, filepath: Path) -> list[Entity]:
        """
        Parse a Python file and extract entities.

        Args:
            filepath: Path to the Python file

        Returns:
            List of extracted Entity objects
        """
        source = filepath.read_text()
        return self.parse(filepath, source)
