# ---
# entity_id: module-agents-router
# entity_name: Task Router
# entity_type_id: module
# entity_path: agents/router.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [TaskRouter, RoutingDecision]
# entity_dependencies: [pydantic, structlog]
# entity_callers: [orchestrator]
# entity_callees: []
# entity_semver_impact: minor
# entity_breaking_change_risk: medium
# ---

"""
Task Router - Intelligent routing between Claude and Ollama.

Routing Logic:
1. Task type classification (code completion, reasoning, etc.)
2. Complexity assessment
3. Context window requirements
4. Quality requirements
5. Cost optimization

The router aims to minimize Claude token usage while maintaining quality
by routing appropriate tasks to local Ollama models.
"""

import re
from dataclasses import dataclass
from typing import Optional

from agents.models import (
    AgentTask,
    AgentType,
    OLLAMA_MODELS,
    OllamaModel,
    TaskComplexity,
    TaskType,
)


@dataclass
class RoutingDecision:
    """Decision about which agent should handle a task."""

    agent_type: AgentType
    model_name: str
    confidence: float  # 0-1 confidence in this routing decision
    reasoning: str
    fallback_agent: Optional[AgentType] = None
    fallback_model: Optional[str] = None


# Tasks that should always go to Claude
CLAUDE_REQUIRED_TASKS = frozenset({
    TaskType.COMPLEX_REASONING,
    TaskType.MULTI_FILE_REFACTOR,
    TaskType.ARCHITECTURE,
    TaskType.SECURITY_ANALYSIS,
    TaskType.COMPLEX_DEBUG,
    TaskType.DESIGN_DECISION,
})

# Tasks that Ollama handles well
OLLAMA_PREFERRED_TASKS = frozenset({
    TaskType.CODE_COMPLETION,
    TaskType.DOCUMENTATION,
    TaskType.SIMPLE_REFACTOR,
    TaskType.TEST_GENERATION,
    TaskType.CODE_EXPLANATION,
    TaskType.EMBEDDING,
    TaskType.SIMPLE_QA,
    TaskType.FORMATTING,
    TaskType.LINTING,
})

# Keywords that suggest Claude is needed
CLAUDE_KEYWORDS = frozenset({
    "security", "vulnerability", "exploit", "architecture",
    "design", "refactor multiple", "across files", "complex",
    "analyze", "review", "audit", "reasoning", "why",
    "trade-off", "tradeoff", "decision", "strategy",
})

# Keywords that suggest Ollama is sufficient
OLLAMA_KEYWORDS = frozenset({
    "complete", "completion", "finish", "simple", "basic",
    "docstring", "comment", "format", "lint", "test",
    "explain", "what does", "how does", "generate",
    "template", "boilerplate", "scaffold",
})


class TaskRouter:
    """
    Routes tasks between Claude and Ollama based on task characteristics.

    The router uses a multi-factor scoring system:
    1. Task type matching
    2. Complexity assessment
    3. Keyword analysis
    4. Context requirements
    5. Quality thresholds
    """

    def __init__(
        self,
        quality_threshold: float = 0.7,
        prefer_local: bool = True,
        available_models: Optional[dict[str, OllamaModel]] = None,
    ):
        """
        Initialize the router.

        Args:
            quality_threshold: Minimum quality score (0-1) for Ollama routing
            prefer_local: If True, prefer Ollama when quality is acceptable
            available_models: Available Ollama models (defaults to OLLAMA_MODELS)
        """
        self.quality_threshold = quality_threshold
        self.prefer_local = prefer_local
        self.available_models = available_models or OLLAMA_MODELS

    def route(self, task: AgentTask) -> RoutingDecision:
        """
        Determine the best agent for a task.

        Args:
            task: The task to route

        Returns:
            RoutingDecision with agent selection and reasoning
        """
        # Check for explicit routing requirements
        if task.require_claude:
            return RoutingDecision(
                agent_type=AgentType.CLAUDE,
                model_name="claude-sonnet-4-20250514",
                confidence=1.0,
                reasoning="Task explicitly requires Claude",
            )

        if not task.allow_ollama:
            return RoutingDecision(
                agent_type=AgentType.CLAUDE,
                model_name="claude-sonnet-4-20250514",
                confidence=1.0,
                reasoning="Ollama routing disabled for this task",
            )

        # Check if task type requires Claude
        if task.task_type in CLAUDE_REQUIRED_TASKS:
            return RoutingDecision(
                agent_type=AgentType.CLAUDE,
                model_name="claude-sonnet-4-20250514",
                confidence=0.95,
                reasoning=f"Task type '{task.task_type.value}' requires Claude's capabilities",
            )

        # Check complexity
        if task.complexity in (TaskComplexity.COMPLEX, TaskComplexity.EXPERT):
            return RoutingDecision(
                agent_type=AgentType.CLAUDE,
                model_name="claude-sonnet-4-20250514",
                confidence=0.9,
                reasoning=f"High complexity ({task.complexity.value}) requires Claude",
                fallback_agent=None,
            )

        # Analyze prompt for keywords
        claude_score = self._calculate_claude_score(task)
        ollama_score = self._calculate_ollama_score(task)

        # Find best Ollama model for this task
        best_ollama = self._find_best_ollama_model(task)

        if best_ollama is None:
            return RoutingDecision(
                agent_type=AgentType.CLAUDE,
                model_name="claude-sonnet-4-20250514",
                confidence=0.8,
                reasoning="No suitable Ollama model available for this task type",
            )

        # Calculate final routing decision
        if task.task_type in OLLAMA_PREFERRED_TASKS and self.prefer_local:
            if best_ollama.quality_score >= self.quality_threshold:
                return RoutingDecision(
                    agent_type=AgentType.OLLAMA,
                    model_name=best_ollama.name,
                    confidence=best_ollama.quality_score,
                    reasoning=f"Task type '{task.task_type.value}' handled well by Ollama",
                    fallback_agent=AgentType.CLAUDE,
                    fallback_model="claude-sonnet-4-20250514",
                )

        # Score-based decision
        if ollama_score > claude_score and best_ollama.quality_score >= self.quality_threshold:
            return RoutingDecision(
                agent_type=AgentType.OLLAMA,
                model_name=best_ollama.name,
                confidence=min(ollama_score, best_ollama.quality_score),
                reasoning=f"Keyword analysis favors Ollama (score: {ollama_score:.2f} vs {claude_score:.2f})",
                fallback_agent=AgentType.CLAUDE,
                fallback_model="claude-sonnet-4-20250514",
            )

        # Default to Claude for safety
        return RoutingDecision(
            agent_type=AgentType.CLAUDE,
            model_name="claude-sonnet-4-20250514",
            confidence=0.85,
            reasoning="Default routing to Claude for best quality",
        )

    def _calculate_claude_score(self, task: AgentTask) -> float:
        """Calculate score indicating task should go to Claude."""
        text = (task.prompt + " " + (task.context or "")).lower()
        matches = sum(1 for kw in CLAUDE_KEYWORDS if kw in text)
        base_score = min(matches * 0.15, 0.9)

        # Adjust for complexity
        complexity_bonus = {
            TaskComplexity.TRIVIAL: -0.2,
            TaskComplexity.SIMPLE: -0.1,
            TaskComplexity.MODERATE: 0.0,
            TaskComplexity.COMPLEX: 0.2,
            TaskComplexity.EXPERT: 0.3,
        }
        score = base_score + complexity_bonus.get(task.complexity, 0)

        # Adjust for file count (more files = more complex)
        if len(task.files) > 3:
            score += 0.15
        elif len(task.files) > 1:
            score += 0.05

        return max(0.0, min(1.0, score))

    def _calculate_ollama_score(self, task: AgentTask) -> float:
        """Calculate score indicating task should go to Ollama."""
        text = (task.prompt + " " + (task.context or "")).lower()
        matches = sum(1 for kw in OLLAMA_KEYWORDS if kw in text)
        base_score = min(matches * 0.15, 0.9)

        # Adjust for complexity (simpler = better for Ollama)
        complexity_bonus = {
            TaskComplexity.TRIVIAL: 0.3,
            TaskComplexity.SIMPLE: 0.2,
            TaskComplexity.MODERATE: 0.0,
            TaskComplexity.COMPLEX: -0.2,
            TaskComplexity.EXPERT: -0.4,
        }
        score = base_score + complexity_bonus.get(task.complexity, 0)

        # Adjust for prompt length (shorter = better for Ollama)
        prompt_len = len(task.prompt)
        if prompt_len < 200:
            score += 0.1
        elif prompt_len > 1000:
            score -= 0.1

        return max(0.0, min(1.0, score))

    def _find_best_ollama_model(self, task: AgentTask) -> Optional[OllamaModel]:
        """Find the best Ollama model for a given task type."""
        candidates = []

        for model in self.available_models.values():
            if task.task_type in model.capabilities:
                candidates.append(model)

        if not candidates:
            return None

        # Prefer models where this task type is in preferred_for
        preferred = [m for m in candidates if task.task_type in m.preferred_for]
        if preferred:
            return max(preferred, key=lambda m: m.quality_score)

        return max(candidates, key=lambda m: m.quality_score)

    def classify_task_type(self, prompt: str, context: Optional[str] = None) -> TaskType:
        """
        Classify a prompt into a task type.

        Args:
            prompt: The task prompt
            context: Optional additional context

        Returns:
            Inferred TaskType
        """
        text = (prompt + " " + (context or "")).lower()

        # Code completion patterns
        if re.search(r"complete|finish|continue|fill in", text):
            return TaskType.CODE_COMPLETION

        # Documentation patterns
        if re.search(r"docstring|document|readme|comment", text):
            return TaskType.DOCUMENTATION

        # Test generation patterns
        if re.search(r"test|unittest|pytest|spec", text):
            return TaskType.TEST_GENERATION

        # Code explanation patterns
        if re.search(r"explain|what does|how does|understand", text):
            return TaskType.CODE_EXPLANATION

        # Security patterns
        if re.search(r"security|vulnerab|exploit|attack|audit", text):
            return TaskType.SECURITY_ANALYSIS

        # Architecture patterns
        if re.search(r"architect|design|structure|pattern|diagram", text):
            return TaskType.ARCHITECTURE

        # Refactoring patterns
        if re.search(r"refactor|restructure|reorganize|clean up", text):
            if re.search(r"multiple|across|all files", text):
                return TaskType.MULTI_FILE_REFACTOR
            return TaskType.SIMPLE_REFACTOR

        # Code review patterns
        if re.search(r"review|feedback|improve|suggest", text):
            return TaskType.CODE_REVIEW

        # Debug patterns
        if re.search(r"debug|fix|error|bug|issue", text):
            if re.search(r"complex|hard|difficult|tricky", text):
                return TaskType.COMPLEX_DEBUG
            return TaskType.GENERAL

        # Formatting/linting patterns
        if re.search(r"format|lint|style|prettier|ruff", text):
            return TaskType.FORMATTING

        return TaskType.GENERAL

    def estimate_complexity(self, prompt: str, context: Optional[str] = None) -> TaskComplexity:
        """
        Estimate task complexity from prompt analysis.

        Args:
            prompt: The task prompt
            context: Optional additional context

        Returns:
            Estimated TaskComplexity
        """
        text = (prompt + " " + (context or "")).lower()

        # Expert indicators
        if re.search(r"complex|difficult|challenging|advanced|expert", text):
            return TaskComplexity.COMPLEX

        # Simple indicators
        if re.search(r"simple|basic|quick|easy|trivial", text):
            return TaskComplexity.SIMPLE

        # Length-based heuristic
        if len(prompt) < 100:
            return TaskComplexity.SIMPLE
        elif len(prompt) < 500:
            return TaskComplexity.MODERATE
        else:
            return TaskComplexity.COMPLEX
