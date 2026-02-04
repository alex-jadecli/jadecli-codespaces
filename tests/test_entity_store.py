# ---
# entity_id: test-entity-store
# entity_name: Entity Store Tests
# entity_type_id: module
# entity_path: tests/test_entity_store.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T16:00:00Z
# entity_exports: []
# entity_dependencies: [entity_store, pytest]
# ---

"""
Tests for entity store functionality.

Test coverage:
- Entity model validation
- Python parser extraction
- TypeScript parser extraction
- Markdown parser extraction
- Registry CRUD operations
- Query interface
- Cache operations
"""

from pathlib import Path
from uuid import UUID

import pytest

from entity_store.models import Entity, EntityState, EntityType


class TestEntityModel:
    """Tests for Entity Pydantic model."""

    def test_entity_creation_minimal(self) -> None:
        """Test creating an entity with minimal required fields."""
        entity = Entity(
            entity_name="TestClass",
            entity_type_id=EntityType.CLASS,
            entity_path="test/file.py",
            entity_line_start=1,
        )
        assert entity.entity_name == "TestClass"
        assert entity.entity_type_id == EntityType.CLASS
        assert entity.entity_state == EntityState.ACTIVE
        assert isinstance(entity.entity_id, UUID)

    def test_entity_creation_full(self) -> None:
        """Test creating an entity with all fields."""
        entity = Entity(
            entity_name="TestFunction",
            entity_type_id=EntityType.FUNCTION,
            entity_path="test/file.py",
            entity_line_start=10,
            entity_line_end=20,
            entity_language="python",
            entity_signature="def test_function(arg: str) -> bool",
            entity_docstring="Test function docstring.",
        )
        assert entity.entity_line_end == 20
        assert entity.entity_signature is not None

    def test_compute_signature(self) -> None:
        """Test signature computation for change detection."""
        sig1 = Entity.compute_signature("path.py", "name", "class", "source1")
        sig2 = Entity.compute_signature("path.py", "name", "class", "source1")
        sig3 = Entity.compute_signature("path.py", "name", "class", "source2")

        assert sig1 == sig2  # Same inputs = same signature
        assert sig1 != sig3  # Different source = different signature

    def test_to_search_text(self) -> None:
        """Test search text generation."""
        entity = Entity(
            entity_name="SearchableClass",
            entity_type_id=EntityType.CLASS,
            entity_path="module/searchable.py",
            entity_line_start=1,
            entity_docstring="A class for searching things.",
        )
        text = entity.to_search_text()
        assert "SearchableClass" in text
        assert "module/searchable.py" in text
        assert "searching things" in text


class TestPythonParser:
    """Tests for Python AST parser."""

    def test_parse_class(self) -> None:
        """Test parsing a Python class definition."""
        from pathlib import Path

        from entity_store.parsers.python_parser import PythonParser

        source = '''
class MyClass:
    """A test class."""
    pass
'''
        parser = PythonParser()
        entities = parser.parse(Path("test.py"), source.strip())

        assert len(entities) == 1
        assert entities[0].entity_name == "MyClass"
        assert entities[0].entity_type_id == EntityType.CLASS
        assert entities[0].entity_docstring == "A test class."
        assert entities[0].entity_line_start == 1

    def test_parse_function(self) -> None:
        """Test parsing a Python function definition."""
        from pathlib import Path

        from entity_store.parsers.python_parser import PythonParser

        source = '''
def my_function(arg1: str, arg2: int) -> bool:
    """A test function."""
    return True
'''
        parser = PythonParser()
        entities = parser.parse(Path("test.py"), source.strip())

        assert len(entities) == 1
        assert entities[0].entity_name == "my_function"
        assert entities[0].entity_type_id == EntityType.FUNCTION
        assert entities[0].entity_docstring == "A test function."
        assert "arg1" in entities[0].entity_signature
        assert "arg2" in entities[0].entity_signature

    def test_parse_method(self) -> None:
        """Test parsing a Python method definition."""
        from pathlib import Path

        from entity_store.parsers.python_parser import PythonParser

        source = '''
class MyClass:
    """A test class."""

    def my_method(self, arg: str) -> None:
        """A test method."""
        pass
'''
        parser = PythonParser()
        entities = parser.parse(Path("test.py"), source.strip())

        # Should get class + method
        assert len(entities) >= 2
        class_entity = next(e for e in entities if e.entity_type_id == EntityType.CLASS)
        method_entity = next(
            e for e in entities if e.entity_type_id == EntityType.METHOD
        )

        assert class_entity.entity_name == "MyClass"
        assert method_entity.entity_name == "my_method"
        assert method_entity.entity_parent_id == class_entity.entity_id

    def test_parse_nested_class(self) -> None:
        """Test parsing nested class definitions."""
        from pathlib import Path

        from entity_store.parsers.python_parser import PythonParser

        source = '''
class OuterClass:
    """Outer class."""

    class InnerClass:
        """Inner class."""
        pass
'''
        parser = PythonParser()
        entities = parser.parse(Path("test.py"), source.strip())

        assert len(entities) == 2
        outer = next(e for e in entities if e.entity_name == "OuterClass")
        inner = next(e for e in entities if e.entity_name == "InnerClass")

        assert inner.entity_parent_id == outer.entity_id

    def test_parse_async_function(self) -> None:
        """Test parsing async function definitions."""
        from pathlib import Path

        from entity_store.parsers.python_parser import PythonParser

        source = '''
async def async_function() -> None:
    """An async function."""
    pass
'''
        parser = PythonParser()
        entities = parser.parse(Path("test.py"), source.strip())

        assert len(entities) == 1
        assert entities[0].entity_name == "async_function"
        assert entities[0].entity_type_id == EntityType.FUNCTION


class TestTypeScriptParser:
    """Tests for TypeScript parser."""

    def test_parse_class(self) -> None:
        """Test parsing a TypeScript class definition."""
        pytest.skip("Parser not yet implemented")

    def test_parse_function(self) -> None:
        """Test parsing a TypeScript function definition."""
        pytest.skip("Parser not yet implemented")

    def test_parse_interface(self) -> None:
        """Test parsing a TypeScript interface definition."""
        pytest.skip("Parser not yet implemented")

    def test_parse_react_component(self) -> None:
        """Test parsing a React component definition."""
        pytest.skip("Parser not yet implemented")


class TestMarkdownParser:
    """Tests for Markdown parser."""

    def test_parse_frontmatter(self) -> None:
        """Test parsing YAML frontmatter."""
        pytest.skip("Parser not yet implemented")

    def test_parse_headings(self) -> None:
        """Test parsing Markdown headings."""
        pytest.skip("Parser not yet implemented")

    def test_parse_code_blocks(self) -> None:
        """Test parsing fenced code blocks."""
        pytest.skip("Parser not yet implemented")


class TestEntityRegistry:
    """Tests for entity registry operations."""

    def test_register_entity(self) -> None:
        """Test registering a new entity."""
        from entity_store.neon_client import NeonClient
        from entity_store.registry import EntityRegistry

        client = NeonClient()
        registry = EntityRegistry(client)

        entity = Entity(
            entity_name="TestClass",
            entity_type_id=EntityType.CLASS,
            entity_path="test/file.py",
            entity_line_start=1,
        )

        entity_id = registry.register(entity)
        assert entity_id == entity.entity_id

        # Verify entity is in registry
        retrieved = registry.get(entity_id)
        assert retrieved is not None
        assert retrieved.entity_name == "TestClass"

    def test_get_entity(self) -> None:
        """Test retrieving an entity by ID."""
        from entity_store.neon_client import NeonClient
        from entity_store.registry import EntityRegistry

        client = NeonClient()
        registry = EntityRegistry(client)

        entity = Entity(
            entity_name="TestFunction",
            entity_type_id=EntityType.FUNCTION,
            entity_path="test/file.py",
            entity_line_start=1,
        )

        entity_id = registry.register(entity)
        retrieved = registry.get(entity_id)

        assert retrieved is not None
        assert retrieved.entity_id == entity_id

        # Test non-existent entity
        from uuid import uuid4

        non_existent = registry.get(uuid4())
        assert non_existent is None

    def test_filter_by_type(self) -> None:
        """Test filtering entities by type."""
        from entity_store.neon_client import NeonClient
        from entity_store.registry import EntityRegistry

        client = NeonClient()
        registry = EntityRegistry(client)

        # Register multiple entities
        class_entity = Entity(
            entity_name="TestClass",
            entity_type_id=EntityType.CLASS,
            entity_path="test/file.py",
            entity_line_start=1,
        )
        func_entity = Entity(
            entity_name="TestFunction",
            entity_type_id=EntityType.FUNCTION,
            entity_path="test/file.py",
            entity_line_start=10,
        )

        registry.register(class_entity)
        registry.register(func_entity)

        # Filter by type
        classes = registry.filter(type_id=EntityType.CLASS)
        assert len(classes) == 1
        assert classes[0].entity_name == "TestClass"

        functions = registry.filter(type_id=EntityType.FUNCTION)
        assert len(functions) == 1
        assert functions[0].entity_name == "TestFunction"

    def test_update_entity(self) -> None:
        """Test updating an entity."""
        from entity_store.neon_client import NeonClient
        from entity_store.registry import EntityRegistry

        client = NeonClient()
        registry = EntityRegistry(client)

        entity = Entity(
            entity_name="TestClass",
            entity_type_id=EntityType.CLASS,
            entity_path="test/file.py",
            entity_line_start=1,
        )

        entity_id = registry.register(entity)

        # Update entity
        updated = registry.update(entity_id, entity_docstring="Updated docstring")
        assert updated.entity_docstring == "Updated docstring"

        # Verify update persisted
        retrieved = registry.get(entity_id)
        assert retrieved.entity_docstring == "Updated docstring"

    def test_archive_entity(self) -> None:
        """Test archiving an entity."""
        from entity_store.neon_client import NeonClient
        from entity_store.registry import EntityRegistry

        client = NeonClient()
        registry = EntityRegistry(client)

        entity = Entity(
            entity_name="TestClass",
            entity_type_id=EntityType.CLASS,
            entity_path="test/file.py",
            entity_line_start=1,
        )

        entity_id = registry.register(entity)

        # Archive entity
        registry.archive(entity_id)

        # Verify entity state is archived
        retrieved = registry.get(entity_id)
        assert retrieved.entity_state == EntityState.ARCHIVED

    def test_parse_file_python(self) -> None:
        """Test parsing a Python file."""
        import tempfile

        from entity_store.neon_client import NeonClient
        from entity_store.registry import EntityRegistry

        client = NeonClient()
        registry = EntityRegistry(client)

        # Create temp Python file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write('''
class MyClass:
    """A test class."""
    pass
''')
            filepath = Path(f.name)

        try:
            entities = registry.parse_file(filepath)
            assert len(entities) == 1
            assert entities[0].entity_name == "MyClass"
            assert entities[0].entity_type_id == EntityType.CLASS
        finally:
            filepath.unlink()


class TestEntityQuery:
    """Tests for GraphQL-like query interface."""

    def test_query_with_type_filter(self) -> None:
        """Test querying with type filter."""
        pytest.skip("Query not yet implemented")

    def test_query_with_field_projection(self) -> None:
        """Test querying with field projection."""
        pytest.skip("Query not yet implemented")

    def test_search_full_text(self) -> None:
        """Test full-text search."""
        pytest.skip("Query not yet implemented")


class TestEntityCache:
    """Tests for caching layer."""

    def test_cache_set_get(self) -> None:
        """Test basic cache set and get."""
        pytest.skip("Cache not yet implemented")

    def test_cache_expiration(self) -> None:
        """Test cache entry expiration."""
        pytest.skip("Cache not yet implemented")

    def test_cache_invalidation(self) -> None:
        """Test cache invalidation."""
        pytest.skip("Cache not yet implemented")
