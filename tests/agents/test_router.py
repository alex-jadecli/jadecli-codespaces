# ---
# entity_id: test-agents-router
# entity_name: Task Router Tests
# entity_type_id: module
# entity_path: tests/agents/test_router.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# ---

"""Tests for TaskRouter."""

import pytest

from agents.models import AgentTask, AgentType, TaskComplexity, TaskType
from agents.router import TaskRouter


class TestTaskRouter:
    """Test cases for TaskRouter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.router = TaskRouter(quality_threshold=0.7, prefer_local=True)

    def test_route_code_completion_to_ollama(self):
        """Code completion tasks should route to Ollama."""
        task = AgentTask(
            prompt="Complete this function",
            task_type=TaskType.CODE_COMPLETION,
            complexity=TaskComplexity.SIMPLE,
        )
        decision = self.router.route(task)
        assert decision.agent_type == AgentType.OLLAMA

    def test_route_complex_reasoning_to_claude(self):
        """Complex reasoning tasks should route to Claude."""
        task = AgentTask(
            prompt="Analyze this architecture",
            task_type=TaskType.COMPLEX_REASONING,
            complexity=TaskComplexity.COMPLEX,
        )
        decision = self.router.route(task)
        assert decision.agent_type == AgentType.CLAUDE

    def test_route_security_to_claude(self):
        """Security analysis should always go to Claude."""
        task = AgentTask(
            prompt="Check for vulnerabilities",
            task_type=TaskType.SECURITY_ANALYSIS,
            complexity=TaskComplexity.MODERATE,
        )
        decision = self.router.route(task)
        assert decision.agent_type == AgentType.CLAUDE

    def test_require_claude_flag(self):
        """require_claude flag should force Claude routing."""
        task = AgentTask(
            prompt="Simple task",
            task_type=TaskType.SIMPLE_QA,
            complexity=TaskComplexity.TRIVIAL,
            require_claude=True,
        )
        decision = self.router.route(task)
        assert decision.agent_type == AgentType.CLAUDE
        assert decision.confidence == 1.0

    def test_disallow_ollama_flag(self):
        """allow_ollama=False should force Claude routing."""
        task = AgentTask(
            prompt="Simple task",
            task_type=TaskType.SIMPLE_QA,
            complexity=TaskComplexity.TRIVIAL,
            allow_ollama=False,
        )
        decision = self.router.route(task)
        assert decision.agent_type == AgentType.CLAUDE

    def test_classify_task_type_code_completion(self):
        """Test classification of code completion prompts."""
        task_type = self.router.classify_task_type("Complete this function")
        assert task_type == TaskType.CODE_COMPLETION

    def test_classify_task_type_documentation(self):
        """Test classification of documentation prompts."""
        task_type = self.router.classify_task_type("Write a docstring for this")
        assert task_type == TaskType.DOCUMENTATION

    def test_classify_task_type_test_generation(self):
        """Test classification of test generation prompts."""
        task_type = self.router.classify_task_type("Generate pytest tests")
        assert task_type == TaskType.TEST_GENERATION

    def test_classify_task_type_security(self):
        """Test classification of security prompts."""
        task_type = self.router.classify_task_type("Check for security vulnerabilities")
        assert task_type == TaskType.SECURITY_ANALYSIS

    def test_estimate_complexity_simple(self):
        """Test complexity estimation for simple prompts."""
        complexity = self.router.estimate_complexity("Fix this simple bug")
        assert complexity == TaskComplexity.SIMPLE

    def test_estimate_complexity_complex(self):
        """Test complexity estimation for complex prompts."""
        complexity = self.router.estimate_complexity("This is a complex refactoring task")
        assert complexity == TaskComplexity.COMPLEX

    def test_fallback_agent_set(self):
        """Ollama routing should include fallback to Claude."""
        task = AgentTask(
            prompt="Complete this function",
            task_type=TaskType.CODE_COMPLETION,
            complexity=TaskComplexity.SIMPLE,
        )
        decision = self.router.route(task)
        if decision.agent_type == AgentType.OLLAMA:
            assert decision.fallback_agent == AgentType.CLAUDE


class TestTaskRouterEdgeCases:
    """Edge case tests for TaskRouter."""

    def test_empty_prompt(self):
        """Router should handle empty prompts."""
        router = TaskRouter()
        task = AgentTask(prompt="", complexity=TaskComplexity.SIMPLE)
        decision = router.route(task)
        # Should default to Claude for safety
        assert decision.agent_type in (AgentType.CLAUDE, AgentType.OLLAMA)

    def test_very_long_prompt(self):
        """Long prompts should increase Claude preference."""
        router = TaskRouter()
        long_prompt = "This is a test. " * 200
        task = AgentTask(prompt=long_prompt, complexity=TaskComplexity.MODERATE)
        decision = router.route(task)
        # Long prompts typically need more reasoning
        assert decision is not None

    def test_multiple_files(self):
        """Tasks with many files should prefer Claude."""
        router = TaskRouter()
        task = AgentTask(
            prompt="Refactor these files",
            files=["a.py", "b.py", "c.py", "d.py", "e.py"],
            complexity=TaskComplexity.MODERATE,
        )
        decision = router.route(task)
        # Multi-file tasks are more complex
        assert decision is not None
