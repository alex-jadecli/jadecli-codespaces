# ---
# entity_id: module-parallel-api
# entity_name: Parallel.ai API Package
# entity_type_id: module
# entity_path: parallel_api/__init__.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [ParallelClient, ParallelMCPServer]
# entity_dependencies: [models, clients, mcp_server]
# entity_callers: [cli, entity_store]
# entity_callees: []
# entity_semver_impact: minor
# entity_breaking_change_risk: low
# entity_actors: [dev, claude]
# ---

"""
Parallel.ai API Package - FastAPI and FastMCP implementations.

Provides:
- Pydantic models for all Parallel.ai API schemas
- Async HTTP client for API calls
- FastMCP server for Claude tool integration
- Support for Extract, Search, Monitor, Tasks, and FindAll APIs

Usage:
    from parallel_api import ParallelClient
    from cli.settings import settings

    client = ParallelClient(api_key=settings.parallel_apikey)
    results = await client.search(objective="Find AI companies")
"""

from parallel_api.clients.async_client import ParallelClient
from parallel_api.models import (
    # Extract
    ExtractRequest,
    ExtractResponse,
    # Search
    SearchRequest,
    SearchResponse,
    # Monitor
    Monitor,
    CreateMonitorRequest,
    # Tasks
    TaskRunRequest,
    TaskRun,
    # FindAll
    FindAllRequest,
    FindAllRun,
)

__all__ = [
    "ParallelClient",
    # Extract
    "ExtractRequest",
    "ExtractResponse",
    # Search
    "SearchRequest",
    "SearchResponse",
    # Monitor
    "Monitor",
    "CreateMonitorRequest",
    # Tasks
    "TaskRunRequest",
    "TaskRun",
    # FindAll
    "FindAllRequest",
    "FindAllRun",
]

__version__ = "0.1.0"
