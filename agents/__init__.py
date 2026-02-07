# ---
# entity_id: module-agents
# entity_name: Multi-Agent Orchestration Module
# entity_type_id: module
# entity_path: agents/__init__.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [AgentOrchestrator, TaskRouter, OllamaClient, AgentTask]
# entity_dependencies: [anthropic, ollama, structlog]
# entity_callers: [cli, hooks]
# entity_callees: [ollama, anthropic]
# entity_semver_impact: major
# entity_breaking_change_risk: high
# entity_actors: [dev, claude]
# ---

"""
Multi-Agent Orchestration Module for Claude + Ollama Workflows.

This module provides:
- Task routing between Claude and Ollama based on task characteristics
- Token usage optimization and tracking
- Parallel task execution with agent coordination
- Rich logging and observability

Architecture:
    ┌─────────────────┐
    │  TaskRouter     │ ← Classifies tasks by complexity/type
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │  Orchestrator   │ ← Routes to appropriate agent
    └────────┬────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼───┐       ┌─────▼─────┐
│ Claude │       │  Ollama   │
│ (API)  │       │  (Local)  │
└────────┘       └───────────┘

Ollama is preferred for:
- Code completion and suggestions
- Documentation generation
- Simple refactoring
- Test generation
- Code explanation
- Local embeddings
- Simple Q&A

Claude is preferred for:
- Complex reasoning chains
- Multi-file refactoring
- Architecture decisions
- Security analysis
- Complex debugging
- Nuanced code review
"""

from agents.models import AgentTask, TaskComplexity, TaskType
from agents.orchestrator import AgentOrchestrator
from agents.router import TaskRouter
from agents.ollama_client import OllamaClient

__all__ = [
    "AgentOrchestrator",
    "TaskRouter",
    "OllamaClient",
    "AgentTask",
    "TaskComplexity",
    "TaskType",
]
