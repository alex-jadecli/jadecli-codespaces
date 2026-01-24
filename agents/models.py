# ---
# entity_id: module-agents-models
# entity_name: Agent Task Models
# entity_type_id: module
# entity_path: agents/models.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [AgentTask, TaskComplexity, TaskType, AgentResponse, TokenUsage]
# entity_dependencies: [pydantic]
# entity_callers: [orchestrator, router]
# entity_callees: []
# entity_semver_impact: major
# entity_breaking_change_risk: high
# ---

"""
Data models for multi-agent task routing and execution.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskType(str, Enum):
    """Classification of task types for routing decisions."""

    # Ollama-preferred tasks (fast, local, low-cost)
    CODE_COMPLETION = "code_completion"
    DOCUMENTATION = "documentation"
    SIMPLE_REFACTOR = "simple_refactor"
    TEST_GENERATION = "test_generation"
    CODE_EXPLANATION = "code_explanation"
    EMBEDDING = "embedding"
    SIMPLE_QA = "simple_qa"
    FORMATTING = "formatting"
    LINTING = "linting"

    # Claude-preferred tasks (complex reasoning required)
    COMPLEX_REASONING = "complex_reasoning"
    MULTI_FILE_REFACTOR = "multi_file_refactor"
    ARCHITECTURE = "architecture"
    SECURITY_ANALYSIS = "security_analysis"
    COMPLEX_DEBUG = "complex_debug"
    CODE_REVIEW = "code_review"
    DESIGN_DECISION = "design_decision"

    # Neutral (can go either way)
    GENERAL = "general"


class TaskComplexity(str, Enum):
    """Complexity levels for task classification."""

    TRIVIAL = "trivial"      # Single-step, obvious solution
    SIMPLE = "simple"        # Few steps, straightforward
    MODERATE = "moderate"    # Multiple steps, some reasoning
    COMPLEX = "complex"      # Many steps, significant reasoning
    EXPERT = "expert"        # Deep expertise required


class AgentType(str, Enum):
    """Available agent types."""

    CLAUDE = "claude"
    OLLAMA = "ollama"
    HYBRID = "hybrid"  # Uses both


class TokenUsage(BaseModel):
    """Token usage tracking for cost optimization."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0

    # Provider breakdown
    claude_tokens: int = 0
    ollama_tokens: int = 0
    tokens_saved: int = 0  # Tokens that would have been Claude but went to Ollama

    def add(self, other: "TokenUsage") -> "TokenUsage":
        """Add token usage from another response."""
        return TokenUsage(
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
            estimated_cost_usd=self.estimated_cost_usd + other.estimated_cost_usd,
            claude_tokens=self.claude_tokens + other.claude_tokens,
            ollama_tokens=self.ollama_tokens + other.ollama_tokens,
            tokens_saved=self.tokens_saved + other.tokens_saved,
        )


class AgentTask(BaseModel):
    """A task to be executed by an agent."""

    id: UUID = Field(default_factory=uuid4)
    task_type: TaskType = TaskType.GENERAL
    complexity: TaskComplexity = TaskComplexity.MODERATE

    # Task content
    prompt: str
    context: Optional[str] = None
    files: list[str] = Field(default_factory=list)

    # Routing hints
    preferred_agent: Optional[AgentType] = None
    require_claude: bool = False  # Force Claude even if Ollama could handle it
    allow_ollama: bool = True     # Allow Ollama routing

    # Execution metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    priority: int = Field(default=5, ge=1, le=10)
    timeout_seconds: int = Field(default=60, ge=1, le=600)

    # Parent task for sub-task tracking
    parent_task_id: Optional[UUID] = None

    model_config = {"frozen": False}


class AgentResponse(BaseModel):
    """Response from an agent execution."""

    task_id: UUID
    agent_type: AgentType
    model_name: str

    # Response content
    content: str
    structured_output: Optional[dict[str, Any]] = None

    # Execution metadata
    started_at: datetime
    completed_at: datetime
    duration_seconds: float

    # Token tracking
    token_usage: TokenUsage

    # Quality indicators
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    needs_review: bool = False
    fallback_used: bool = False  # True if fell back to different agent

    @property
    def latency_ms(self) -> float:
        """Get latency in milliseconds."""
        return self.duration_seconds * 1000


class OllamaModel(BaseModel):
    """Configuration for an Ollama model."""

    name: str
    capabilities: list[TaskType]
    max_context: int = 4096
    preferred_for: list[TaskType] = Field(default_factory=list)

    # Performance characteristics
    tokens_per_second: float = 50.0
    quality_score: float = 0.7  # 0-1 scale vs Claude


# Default Ollama model configurations
OLLAMA_MODELS: dict[str, OllamaModel] = {
    "codellama:7b": OllamaModel(
        name="codellama:7b",
        capabilities=[
            TaskType.CODE_COMPLETION,
            TaskType.SIMPLE_REFACTOR,
            TaskType.TEST_GENERATION,
            TaskType.CODE_EXPLANATION,
            TaskType.FORMATTING,
        ],
        max_context=4096,
        preferred_for=[TaskType.CODE_COMPLETION, TaskType.TEST_GENERATION],
        tokens_per_second=60.0,
        quality_score=0.75,
    ),
    "llama3.2:3b": OllamaModel(
        name="llama3.2:3b",
        capabilities=[
            TaskType.SIMPLE_QA,
            TaskType.DOCUMENTATION,
            TaskType.CODE_EXPLANATION,
            TaskType.GENERAL,
        ],
        max_context=8192,
        preferred_for=[TaskType.SIMPLE_QA, TaskType.DOCUMENTATION],
        tokens_per_second=100.0,
        quality_score=0.65,
    ),
    "nomic-embed-text": OllamaModel(
        name="nomic-embed-text",
        capabilities=[TaskType.EMBEDDING],
        max_context=8192,
        preferred_for=[TaskType.EMBEDDING],
        tokens_per_second=200.0,
        quality_score=0.9,
    ),
}
