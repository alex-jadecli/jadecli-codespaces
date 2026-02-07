# ---
# entity_id: module-agents-orchestrator
# entity_name: Agent Orchestrator
# entity_type_id: module
# entity_path: agents/orchestrator.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [AgentOrchestrator]
# entity_dependencies: [anthropic, structlog]
# entity_callers: [cli, hooks]
# entity_callees: [router, ollama_client, claude_api]
# entity_semver_impact: major
# entity_breaking_change_risk: high
# entity_actors: [dev, claude]
# ---

"""
Agent Orchestrator - Coordinates multi-agent task execution.

This module provides the main orchestration layer that:
1. Accepts tasks from various sources
2. Routes them to appropriate agents (Claude or Ollama)
3. Manages fallback and retry logic
4. Tracks token usage and costs
5. Provides observability and logging

Architecture:
    ┌─────────────────────────────────────────┐
    │           AgentOrchestrator             │
    │  ┌─────────────────────────────────┐   │
    │  │         TaskRouter              │   │
    │  └──────────────┬──────────────────┘   │
    │                 │                       │
    │    ┌────────────┴────────────┐         │
    │    │                         │         │
    │  ┌─▼────────┐          ┌─────▼─────┐   │
    │  │ Claude   │          │  Ollama   │   │
    │  │ Client   │          │  Client   │   │
    │  └──────────┘          └───────────┘   │
    └─────────────────────────────────────────┘
"""

import asyncio
from datetime import datetime
from typing import Any, Callable, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from agents.models import (
    AgentResponse,
    AgentTask,
    AgentType,
    TaskComplexity,
    TaskType,
    TokenUsage,
)
from agents.ollama_client import OllamaClient, OllamaConfig
from agents.router import RoutingDecision, TaskRouter


class OrchestratorConfig(BaseModel):
    """Configuration for the orchestrator."""

    # Routing settings
    quality_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    prefer_local: bool = True

    # Fallback settings
    enable_fallback: bool = True
    max_retries: int = 2

    # Ollama settings
    ollama_base_url: str = "http://localhost:11434"
    ollama_timeout: int = 60

    # Claude settings
    claude_model: str = "claude-sonnet-4-20250514"

    # Observability
    log_level: str = "INFO"
    track_metrics: bool = True


class OrchestratorMetrics(BaseModel):
    """Metrics tracked by the orchestrator."""

    total_tasks: int = 0
    claude_tasks: int = 0
    ollama_tasks: int = 0
    fallback_count: int = 0
    error_count: int = 0

    total_token_usage: TokenUsage = Field(default_factory=TokenUsage)
    tokens_saved: int = 0  # Tokens saved by using Ollama

    # Timing
    total_duration_seconds: float = 0.0
    avg_claude_latency_ms: float = 0.0
    avg_ollama_latency_ms: float = 0.0


class AgentOrchestrator:
    """
    Main orchestrator for multi-agent task execution.

    Coordinates between Claude and Ollama based on task characteristics,
    handles fallback logic, and tracks usage metrics.
    """

    def __init__(
        self,
        config: Optional[OrchestratorConfig] = None,
        claude_client: Optional[Any] = None,  # anthropic.Anthropic
    ):
        """
        Initialize the orchestrator.

        Args:
            config: Orchestrator configuration
            claude_client: Optional pre-configured Claude client
        """
        self.config = config or OrchestratorConfig()
        self._claude_client = claude_client
        self._ollama_client: Optional[OllamaClient] = None
        self._router: Optional[TaskRouter] = None
        self._metrics = OrchestratorMetrics()

        # Task history for observability
        self._task_history: list[tuple[AgentTask, AgentResponse]] = []

        # Callbacks for observability
        self._on_task_start: Optional[Callable[[AgentTask, RoutingDecision], None]] = None
        self._on_task_complete: Optional[Callable[[AgentTask, AgentResponse], None]] = None

    @property
    def router(self) -> TaskRouter:
        """Get or create the task router."""
        if self._router is None:
            self._router = TaskRouter(
                quality_threshold=self.config.quality_threshold,
                prefer_local=self.config.prefer_local,
            )
        return self._router

    @property
    def ollama(self) -> OllamaClient:
        """Get or create the Ollama client."""
        if self._ollama_client is None:
            self._ollama_client = OllamaClient(
                OllamaConfig(
                    base_url=self.config.ollama_base_url,
                    timeout_seconds=self.config.ollama_timeout,
                )
            )
        return self._ollama_client

    @property
    def metrics(self) -> OrchestratorMetrics:
        """Get current metrics."""
        return self._metrics

    async def initialize(self) -> bool:
        """
        Initialize the orchestrator and check agent availability.

        Returns:
            True if at least one agent is available
        """
        ollama_available = await self.ollama.is_available()

        if ollama_available:
            models = await self.ollama.list_models()
            print(f"Ollama available with {len(models)} models")
        else:
            print("Ollama not available - all tasks will route to Claude")

        # Claude is always available if API key is configured
        try:
            from cli.settings import settings
            claude_available = settings.has_parallel_api
        except ImportError:
            claude_available = False

        return ollama_available or claude_available

    async def execute(self, task: AgentTask) -> AgentResponse:
        """
        Execute a task using the appropriate agent.

        Args:
            task: The task to execute

        Returns:
            AgentResponse with execution results
        """
        # Auto-classify if not specified
        if task.task_type == TaskType.GENERAL:
            task.task_type = self.router.classify_task_type(task.prompt, task.context)

        if task.complexity == TaskComplexity.MODERATE:
            task.complexity = self.router.estimate_complexity(task.prompt, task.context)

        # Get routing decision
        decision = self.router.route(task)

        # Notify observers
        if self._on_task_start:
            self._on_task_start(task, decision)

        # Execute with the chosen agent
        self._metrics.total_tasks += 1

        try:
            if decision.agent_type == AgentType.OLLAMA:
                response = await self._execute_ollama(task, decision)
            else:
                response = await self._execute_claude(task, decision)

            # Handle fallback if needed
            if response.needs_review and self.config.enable_fallback and decision.fallback_agent:
                print(f"Falling back from {decision.agent_type} to {decision.fallback_agent}")
                self._metrics.fallback_count += 1

                if decision.fallback_agent == AgentType.CLAUDE:
                    response = await self._execute_claude(task, decision)
                    response.fallback_used = True

        except Exception as e:
            self._metrics.error_count += 1
            response = AgentResponse(
                task_id=task.id,
                agent_type=decision.agent_type,
                model_name=decision.model_name,
                content=f"Error: {str(e)}",
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
                duration_seconds=0.0,
                token_usage=TokenUsage(),
                confidence=0.0,
                needs_review=True,
            )

        # Update metrics
        self._update_metrics(response)

        # Store history
        self._task_history.append((task, response))

        # Notify observers
        if self._on_task_complete:
            self._on_task_complete(task, response)

        return response

    async def _execute_ollama(
        self,
        task: AgentTask,
        decision: RoutingDecision,
    ) -> AgentResponse:
        """Execute task with Ollama."""
        self._metrics.ollama_tasks += 1

        # Check if Ollama is available
        if not await self.ollama.is_available():
            # Fall back to Claude
            if self.config.enable_fallback:
                self._metrics.fallback_count += 1
                return await self._execute_claude(task, decision)
            raise RuntimeError("Ollama not available and fallback disabled")

        response = await self.ollama.execute_task(task, model=decision.model_name)

        # Track tokens saved
        estimated_claude_tokens = len(task.prompt.split()) * 2  # Rough estimate
        self._metrics.tokens_saved += estimated_claude_tokens

        return response

    async def _execute_claude(
        self,
        task: AgentTask,
        decision: RoutingDecision,
    ) -> AgentResponse:
        """Execute task with Claude."""
        self._metrics.claude_tasks += 1
        started_at = datetime.utcnow()

        try:
            from anthropic import Anthropic
            from cli.settings import settings

            if self._claude_client is None:
                self._claude_client = Anthropic(api_key=settings.parallel_apikey)

            # Build messages
            messages = [{"role": "user", "content": task.prompt}]

            # Make API call
            response = self._claude_client.messages.create(
                model=self.config.claude_model,
                max_tokens=4096,
                system=task.context or "You are a helpful coding assistant.",
                messages=messages,
            )

            completed_at = datetime.utcnow()
            content = response.content[0].text if response.content else ""

            # Calculate token usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            # Estimate cost (Sonnet pricing)
            cost = (input_tokens * 0.003 + output_tokens * 0.015) / 1000

            return AgentResponse(
                task_id=task.id,
                agent_type=AgentType.CLAUDE,
                model_name=self.config.claude_model,
                content=content,
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=(completed_at - started_at).total_seconds(),
                token_usage=TokenUsage(
                    prompt_tokens=input_tokens,
                    completion_tokens=output_tokens,
                    total_tokens=input_tokens + output_tokens,
                    claude_tokens=input_tokens + output_tokens,
                    estimated_cost_usd=cost,
                ),
                confidence=0.95,
            )

        except Exception as e:
            completed_at = datetime.utcnow()
            return AgentResponse(
                task_id=task.id,
                agent_type=AgentType.CLAUDE,
                model_name=self.config.claude_model,
                content=f"Error: {str(e)}",
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=(completed_at - started_at).total_seconds(),
                token_usage=TokenUsage(),
                confidence=0.0,
                needs_review=True,
            )

    def _update_metrics(self, response: AgentResponse) -> None:
        """Update orchestrator metrics from a response."""
        self._metrics.total_token_usage = self._metrics.total_token_usage.add(
            response.token_usage
        )
        self._metrics.total_duration_seconds += response.duration_seconds

        # Update average latencies
        if response.agent_type == AgentType.CLAUDE and self._metrics.claude_tasks > 0:
            prev_avg = self._metrics.avg_claude_latency_ms
            new_val = response.latency_ms
            self._metrics.avg_claude_latency_ms = (
                prev_avg * (self._metrics.claude_tasks - 1) + new_val
            ) / self._metrics.claude_tasks

        if response.agent_type == AgentType.OLLAMA and self._metrics.ollama_tasks > 0:
            prev_avg = self._metrics.avg_ollama_latency_ms
            new_val = response.latency_ms
            self._metrics.avg_ollama_latency_ms = (
                prev_avg * (self._metrics.ollama_tasks - 1) + new_val
            ) / self._metrics.ollama_tasks

    def get_usage_summary(self) -> dict[str, Any]:
        """Get a summary of usage statistics."""
        return {
            "total_tasks": self._metrics.total_tasks,
            "claude_tasks": self._metrics.claude_tasks,
            "ollama_tasks": self._metrics.ollama_tasks,
            "ollama_percentage": (
                self._metrics.ollama_tasks / self._metrics.total_tasks * 100
                if self._metrics.total_tasks > 0
                else 0
            ),
            "fallback_count": self._metrics.fallback_count,
            "error_count": self._metrics.error_count,
            "total_tokens": self._metrics.total_token_usage.total_tokens,
            "claude_tokens": self._metrics.total_token_usage.claude_tokens,
            "ollama_tokens": self._metrics.total_token_usage.ollama_tokens,
            "tokens_saved": self._metrics.tokens_saved,
            "estimated_cost_usd": self._metrics.total_token_usage.estimated_cost_usd,
            "avg_claude_latency_ms": self._metrics.avg_claude_latency_ms,
            "avg_ollama_latency_ms": self._metrics.avg_ollama_latency_ms,
        }

    def register_callbacks(
        self,
        on_task_start: Optional[Callable[[AgentTask, RoutingDecision], None]] = None,
        on_task_complete: Optional[Callable[[AgentTask, AgentResponse], None]] = None,
    ) -> None:
        """Register callback functions for observability."""
        self._on_task_start = on_task_start
        self._on_task_complete = on_task_complete


# CLI entry point
def main() -> None:
    """Run the orchestrator in interactive mode."""
    import asyncio

    async def interactive_loop():
        orchestrator = AgentOrchestrator()
        await orchestrator.initialize()

        print("\nMulti-Agent Orchestrator Ready")
        print("Type 'quit' to exit, 'stats' for usage statistics")
        print("-" * 50)

        while True:
            try:
                prompt = input("\nTask> ").strip()
                if prompt.lower() == "quit":
                    break
                if prompt.lower() == "stats":
                    import json
                    print(json.dumps(orchestrator.get_usage_summary(), indent=2))
                    continue
                if not prompt:
                    continue

                task = AgentTask(prompt=prompt)
                response = await orchestrator.execute(task)

                print(f"\n[{response.agent_type.value}:{response.model_name}]")
                print(response.content)
                print(f"\n(tokens: {response.token_usage.total_tokens}, latency: {response.latency_ms:.0f}ms)")

            except KeyboardInterrupt:
                print("\nInterrupted")
                break
            except Exception as e:
                print(f"Error: {e}")

    asyncio.run(interactive_loop())


if __name__ == "__main__":
    main()
