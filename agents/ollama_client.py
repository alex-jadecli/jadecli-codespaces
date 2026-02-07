# ---
# entity_id: module-agents-ollama
# entity_name: Ollama Client
# entity_type_id: module
# entity_path: agents/ollama_client.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [OllamaClient]
# entity_dependencies: [httpx, pydantic]
# entity_callers: [orchestrator]
# entity_callees: [ollama_api]
# entity_semver_impact: minor
# entity_breaking_change_risk: low
# ---

"""
Ollama Client - Async client for local Ollama inference.

Provides a consistent interface for:
- Chat completions
- Embeddings
- Model management
- Health checks
"""

import asyncio
from datetime import datetime
from typing import Any, AsyncIterator, Optional

import httpx
from pydantic import BaseModel, Field

from agents.models import AgentResponse, AgentTask, AgentType, TokenUsage


class OllamaConfig(BaseModel):
    """Configuration for Ollama client."""

    base_url: str = Field(default="http://localhost:11434")
    timeout_seconds: int = Field(default=60)
    default_model: str = Field(default="codellama:7b")
    num_ctx: int = Field(default=4096)  # Context window size


class OllamaMessage(BaseModel):
    """A message in Ollama chat format."""

    role: str  # "system", "user", "assistant"
    content: str


class OllamaClient:
    """
    Async client for Ollama API.

    Provides methods for:
    - Chat completions (generate)
    - Streaming responses
    - Embeddings
    - Model listing and management
    """

    def __init__(self, config: Optional[OllamaConfig] = None):
        """Initialize Ollama client."""
        self.config = config or OllamaConfig()
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "OllamaClient":
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=self.config.timeout_seconds,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client, creating if needed."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.config.base_url,
                timeout=self.config.timeout_seconds,
            )
        return self._client

    async def is_available(self) -> bool:
        """Check if Ollama server is available."""
        try:
            response = await self.client.get("/api/tags")
            return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> list[dict[str, Any]]:
        """List available Ollama models."""
        try:
            response = await self.client.get("/api/tags")
            response.raise_for_status()
            data = response.json()
            return data.get("models", [])
        except Exception:
            return []

    async def has_model(self, model_name: str) -> bool:
        """Check if a specific model is available."""
        models = await self.list_models()
        return any(m.get("name", "").startswith(model_name) for m in models)

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        context: Optional[list[int]] = None,
        options: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Generate a completion.

        Args:
            prompt: The prompt to complete
            model: Model name (defaults to config.default_model)
            system: System prompt
            context: Previous context for continuation
            options: Model options (temperature, top_p, etc.)

        Returns:
            Response dict with 'response', 'context', 'total_duration', etc.
        """
        payload = {
            "model": model or self.config.default_model,
            "prompt": prompt,
            "stream": False,
            "options": options or {"num_ctx": self.config.num_ctx},
        }

        if system:
            payload["system"] = system
        if context:
            payload["context"] = context

        response = await self.client.post("/api/generate", json=payload)
        response.raise_for_status()
        return response.json()

    async def chat(
        self,
        messages: list[OllamaMessage],
        model: Optional[str] = None,
        options: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Chat completion with message history.

        Args:
            messages: List of chat messages
            model: Model name
            options: Model options

        Returns:
            Response dict with 'message', 'total_duration', etc.
        """
        payload = {
            "model": model or self.config.default_model,
            "messages": [m.model_dump() for m in messages],
            "stream": False,
            "options": options or {"num_ctx": self.config.num_ctx},
        }

        response = await self.client.post("/api/chat", json=payload)
        response.raise_for_status()
        return response.json()

    async def stream_generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        options: Optional[dict[str, Any]] = None,
    ) -> AsyncIterator[str]:
        """
        Stream a completion token by token.

        Yields:
            Individual tokens as they're generated
        """
        payload = {
            "model": model or self.config.default_model,
            "prompt": prompt,
            "stream": True,
            "options": options or {"num_ctx": self.config.num_ctx},
        }

        if system:
            payload["system"] = system

        async with self.client.stream("POST", "/api/generate", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line:
                    import json
                    data = json.loads(line)
                    if "response" in data:
                        yield data["response"]
                    if data.get("done", False):
                        break

    async def embeddings(
        self,
        text: str,
        model: str = "nomic-embed-text",
    ) -> list[float]:
        """
        Generate embeddings for text.

        Args:
            text: Text to embed
            model: Embedding model name

        Returns:
            List of embedding floats
        """
        payload = {
            "model": model,
            "prompt": text,
        }

        response = await self.client.post("/api/embeddings", json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("embedding", [])

    async def execute_task(
        self,
        task: AgentTask,
        model: Optional[str] = None,
    ) -> AgentResponse:
        """
        Execute a task and return an AgentResponse.

        Args:
            task: The task to execute
            model: Optional model override

        Returns:
            AgentResponse with execution results
        """
        started_at = datetime.utcnow()
        model_name = model or self.config.default_model

        # Build messages
        messages = []
        if task.context:
            messages.append(OllamaMessage(role="system", content=task.context))
        messages.append(OllamaMessage(role="user", content=task.prompt))

        try:
            result = await self.chat(messages, model=model_name)
            completed_at = datetime.utcnow()

            # Extract response
            content = result.get("message", {}).get("content", "")

            # Calculate token usage (approximate)
            prompt_tokens = result.get("prompt_eval_count", 0)
            completion_tokens = result.get("eval_count", 0)

            return AgentResponse(
                task_id=task.id,
                agent_type=AgentType.OLLAMA,
                model_name=model_name,
                content=content,
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=(completed_at - started_at).total_seconds(),
                token_usage=TokenUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                    ollama_tokens=prompt_tokens + completion_tokens,
                    estimated_cost_usd=0.0,  # Local = free
                ),
                confidence=0.7,  # Default confidence for Ollama
            )

        except Exception as e:
            completed_at = datetime.utcnow()
            return AgentResponse(
                task_id=task.id,
                agent_type=AgentType.OLLAMA,
                model_name=model_name,
                content=f"Error: {str(e)}",
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=(completed_at - started_at).total_seconds(),
                token_usage=TokenUsage(),
                confidence=0.0,
                needs_review=True,
            )

    async def pull_model(self, model_name: str) -> bool:
        """
        Pull a model from Ollama registry.

        Args:
            model_name: Name of model to pull

        Returns:
            True if successful
        """
        try:
            payload = {"name": model_name, "stream": False}
            response = await self.client.post(
                "/api/pull",
                json=payload,
                timeout=600.0,  # Model pulls can take a while
            )
            response.raise_for_status()
            return True
        except Exception:
            return False


# Convenience function for one-off operations
async def get_ollama_client() -> OllamaClient:
    """Get a configured Ollama client."""
    return OllamaClient()
