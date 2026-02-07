# ---
# entity_id: test-agents-models
# entity_name: Agent Model Tests
# entity_type_id: module
# entity_path: tests/agents/test_models.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# ---

"""Tests for agent data models."""

import pytest
from datetime import datetime
from uuid import UUID

from agents.models import (
    AgentResponse,
    AgentTask,
    AgentType,
    OllamaModel,
    TaskComplexity,
    TaskType,
    TokenUsage,
)


class TestAgentTask:
    """Tests for AgentTask model."""

    def test_default_values(self):
        """Test default values are set correctly."""
        task = AgentTask(prompt="Test prompt")
        assert task.task_type == TaskType.GENERAL
        assert task.complexity == TaskComplexity.MODERATE
        assert task.priority == 5
        assert task.allow_ollama is True
        assert task.require_claude is False
        assert isinstance(task.id, UUID)

    def test_with_all_fields(self):
        """Test task with all fields specified."""
        task = AgentTask(
            prompt="Test prompt",
            context="Test context",
            task_type=TaskType.CODE_COMPLETION,
            complexity=TaskComplexity.SIMPLE,
            files=["a.py", "b.py"],
            priority=8,
            timeout_seconds=120,
        )
        assert task.prompt == "Test prompt"
        assert task.context == "Test context"
        assert task.task_type == TaskType.CODE_COMPLETION
        assert len(task.files) == 2
        assert task.priority == 8


class TestTokenUsage:
    """Tests for TokenUsage model."""

    def test_default_values(self):
        """Test default values are zero."""
        usage = TokenUsage()
        assert usage.prompt_tokens == 0
        assert usage.completion_tokens == 0
        assert usage.total_tokens == 0
        assert usage.estimated_cost_usd == 0.0

    def test_add_usage(self):
        """Test adding two TokenUsage objects."""
        usage1 = TokenUsage(
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            claude_tokens=150,
        )
        usage2 = TokenUsage(
            prompt_tokens=200,
            completion_tokens=100,
            total_tokens=300,
            ollama_tokens=300,
        )
        combined = usage1.add(usage2)
        assert combined.prompt_tokens == 300
        assert combined.completion_tokens == 150
        assert combined.total_tokens == 450
        assert combined.claude_tokens == 150
        assert combined.ollama_tokens == 300


class TestAgentResponse:
    """Tests for AgentResponse model."""

    def test_latency_property(self):
        """Test latency_ms calculation."""
        now = datetime.utcnow()
        response = AgentResponse(
            task_id=UUID("12345678-1234-5678-1234-567812345678"),
            agent_type=AgentType.CLAUDE,
            model_name="claude-sonnet",
            content="Test response",
            started_at=now,
            completed_at=now,
            duration_seconds=1.5,
            token_usage=TokenUsage(),
        )
        assert response.latency_ms == 1500.0


class TestOllamaModel:
    """Tests for OllamaModel configuration."""

    def test_model_capabilities(self):
        """Test model capability definition."""
        model = OllamaModel(
            name="codellama:7b",
            capabilities=[TaskType.CODE_COMPLETION, TaskType.TEST_GENERATION],
            max_context=4096,
            quality_score=0.75,
        )
        assert TaskType.CODE_COMPLETION in model.capabilities
        assert model.quality_score == 0.75


class TestTaskType:
    """Tests for TaskType enum."""

    def test_ollama_preferred_types(self):
        """Verify Ollama-preferred task types."""
        ollama_types = [
            TaskType.CODE_COMPLETION,
            TaskType.DOCUMENTATION,
            TaskType.SIMPLE_REFACTOR,
            TaskType.TEST_GENERATION,
        ]
        for task_type in ollama_types:
            assert task_type.value is not None

    def test_claude_preferred_types(self):
        """Verify Claude-preferred task types."""
        claude_types = [
            TaskType.COMPLEX_REASONING,
            TaskType.MULTI_FILE_REFACTOR,
            TaskType.SECURITY_ANALYSIS,
        ]
        for task_type in claude_types:
            assert task_type.value is not None
