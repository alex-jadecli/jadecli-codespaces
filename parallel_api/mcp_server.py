# ---
# entity_id: module-parallel-mcp-server
# entity_name: Parallel.ai MCP Server
# entity_type_id: module
# entity_path: parallel_api/mcp_server.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [ParallelMCPServer, mcp_app]
# entity_dependencies: [fastmcp, clients, models, settings]
# entity_callers: [claude]
# entity_callees: [clients]
# entity_semver_impact: major
# entity_breaking_change_risk: medium
# entity_public_api: true
# entity_actors: [claude, dev]
# ---

"""
FastMCP Server for Parallel.ai API.

Exposes Parallel.ai capabilities as MCP tools for Claude:
- parallel_search: Web search with natural language
- parallel_extract: Extract content from URLs
- parallel_monitor_create: Create web monitors
- parallel_task_run: Run tasks with processors
- parallel_findall: Entity discovery

Usage:
    # Start server
    python -m parallel_api.mcp_server

    # Or via FastMCP CLI
    fastmcp run parallel_api.mcp_server:mcp_app

Configuration:
    Requires PARALLEL_APIKEY in .env or environment.
    Uses cli/settings.py for centralized configuration.
"""

# Import settings for API key
import sys
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from pydantic import Field

sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.settings import settings
from parallel_api.clients.async_client import ParallelClient

# Create FastMCP application
mcp_app = FastMCP(
    name="parallel-ai",
    description="Parallel.ai API tools for web search, extraction, monitoring, and tasks",
)


def get_client() -> ParallelClient:
    """Get configured Parallel.ai client."""
    if not settings.parallel_apikey:
        raise ValueError("PARALLEL_APIKEY not configured. Set it in .env or environment variables.")
    return ParallelClient(api_key=settings.parallel_apikey)


# === Search Tool ===


@mcp_app.tool()
async def parallel_search(
    objective: str = Field(
        ...,
        description="Natural-language description of what to search for",
    ),
    max_results: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results",
    ),
    mode: str = Field(
        default="one-shot",
        description="Search mode: 'one-shot' or 'agentic'",
    ),
) -> dict[str, Any]:
    """
    Search the web using Parallel.ai's intelligent search.

    Returns search results with URLs, titles, and relevant excerpts.
    Use 'agentic' mode for more thorough multi-step searches.
    """
    async with get_client() as client:
        response = await client.search(
            objective=objective,
            max_results=max_results,
            mode=mode,
        )

    return {
        "search_id": response.search_id,
        "results": [
            {
                "url": r.url,
                "title": r.title,
                "excerpts": r.excerpts,
            }
            for r in response.results
        ],
        "result_count": len(response.results),
    }


# === Extract Tool ===


@mcp_app.tool()
async def parallel_extract(
    urls: list[str] = Field(
        ...,
        description="URLs to extract content from",
        min_length=1,
    ),
    objective: str | None = Field(
        default=None,
        description="Focus extraction on this objective",
    ),
    include_full_content: bool = Field(
        default=False,
        description="Include full page content (more tokens)",
    ),
) -> dict[str, Any]:
    """
    Extract content from web URLs using Parallel.ai.

    Returns extracted content with titles and relevant excerpts.
    Optionally focus extraction on a specific objective.
    """
    async with get_client() as client:
        response = await client.extract(
            urls=urls,
            objective=objective,
            excerpts=True,
            full_content=include_full_content,
        )

    return {
        "extract_id": response.extract_id,
        "results": [
            {
                "url": r.url,
                "title": r.title,
                "excerpts": r.excerpts,
                "full_content": r.full_content if include_full_content else None,
            }
            for r in response.results
        ],
        "errors": [{"url": e.url, "error": e.error_type} for e in response.errors],
    }


# === Monitor Tools ===


@mcp_app.tool()
async def parallel_monitor_create(
    query: str = Field(
        ...,
        description="Query to monitor for changes",
    ),
    cadence: str = Field(
        default="daily",
        description="How often to check: 'hourly', 'daily', or 'weekly'",
    ),
) -> dict[str, Any]:
    """
    Create a web monitor that periodically checks for changes.

    Returns monitor details including ID for future reference.
    """
    async with get_client() as client:
        monitor = await client.create_monitor(
            query=query,
            cadence=cadence,
        )

    return {
        "monitor_id": monitor.monitor_id,
        "query": monitor.query,
        "cadence": monitor.cadence.value,
        "status": monitor.status.value,
        "created_at": monitor.created_at.isoformat(),
    }


@mcp_app.tool()
async def parallel_monitor_list() -> dict[str, Any]:
    """
    List all active monitors.

    Returns list of monitors with their status and configuration.
    """
    async with get_client() as client:
        monitors = await client.list_monitors()

    return {
        "monitors": [
            {
                "monitor_id": m.monitor_id,
                "query": m.query,
                "cadence": m.cadence.value,
                "status": m.status.value,
                "last_run_at": m.last_run_at.isoformat() if m.last_run_at else None,
            }
            for m in monitors
        ],
        "count": len(monitors),
    }


@mcp_app.tool()
async def parallel_monitor_delete(
    monitor_id: str = Field(
        ...,
        description="ID of the monitor to delete",
    ),
) -> dict[str, Any]:
    """
    Delete a monitor.

    Stops all future executions. Cannot be undone.
    """
    async with get_client() as client:
        await client.delete_monitor(monitor_id)

    return {
        "deleted": True,
        "monitor_id": monitor_id,
    }


# === Task Tools ===


@mcp_app.tool()
async def parallel_task_run(
    processor: str = Field(
        ...,
        description="Processor to use (e.g., 'gpt-4', 'claude-3')",
    ),
    input_text: str = Field(
        ...,
        description="Task input text",
    ),
    wait_for_completion: bool = Field(
        default=True,
        description="Wait for task to complete before returning",
    ),
) -> dict[str, Any]:
    """
    Run a task using Parallel.ai processors.

    Returns task result or status depending on wait_for_completion.
    """
    async with get_client() as client:
        run = await client.create_task_run(
            processor=processor,
            input=input_text,
        )

        if wait_for_completion:
            run = await client.wait_for_task_run(run.run_id)
            if run.status.value == "completed":
                result = await client.get_task_run_result(run.run_id)
                return {
                    "run_id": run.run_id,
                    "status": run.status.value,
                    "result": result,
                }

    return {
        "run_id": run.run_id,
        "status": run.status.value,
        "is_active": run.is_active,
    }


@mcp_app.tool()
async def parallel_task_status(
    run_id: str = Field(
        ...,
        description="Task run ID to check",
    ),
) -> dict[str, Any]:
    """
    Check the status of a task run.

    Returns current status and result if completed.
    """
    async with get_client() as client:
        run = await client.get_task_run(run_id)

        response = {
            "run_id": run.run_id,
            "status": run.status.value,
            "is_active": run.is_active,
            "processor": run.processor,
        }

        if run.status.value == "completed":
            result = await client.get_task_run_result(run_id)
            response["result"] = result

        if run.error:
            response["error"] = {
                "code": run.error.code,
                "message": run.error.message,
            }

    return response


# === FindAll Tools ===


@mcp_app.tool()
async def parallel_findall(
    objective: str = Field(
        ...,
        description="Natural language objective for entity discovery",
    ),
    entity_type: str = Field(
        ...,
        description="Type of entity to find (e.g., 'company', 'person')",
    ),
    match_limit: int = Field(
        default=50,
        ge=5,
        le=1000,
        description="Maximum number of matches",
    ),
    generator: str = Field(
        default="core",
        description="Processing tier: 'base', 'core', 'pro', or 'preview'",
    ),
) -> dict[str, Any]:
    """
    Find entities matching criteria using Parallel.ai FindAll.

    Returns discovered entities with their data.
    """
    async with get_client() as client:
        run = await client.create_findall_run(
            objective=objective,
            entity_type=entity_type,
            match_conditions=[{"field": "name", "operator": "exists", "value": True}],
            generator=generator,
            match_limit=match_limit,
        )

    return {
        "findall_id": run.findall_id,
        "status": run.status.status.value,
        "is_active": run.status.is_active,
        "generator": run.generator.value,
    }


@mcp_app.tool()
async def parallel_findall_result(
    findall_id: str = Field(
        ...,
        description="FindAll run ID to get results for",
    ),
) -> dict[str, Any]:
    """
    Get results from a FindAll run.

    Returns matched entities with their data.
    """
    async with get_client() as client:
        result = await client.get_findall_result(findall_id)

    return {
        "findall_id": result.findall_id,
        "total_matches": result.total_matches,
        "matches": [
            {
                "entity_id": m.entity_id,
                "entity_type": m.entity_type,
                "data": m.data,
                "confidence": m.confidence,
            }
            for m in result.matches[:20]  # Limit to first 20 for token efficiency
        ],
    }


# === Resources ===


@mcp_app.resource("parallel://config")
async def get_parallel_config() -> str:
    """Get current Parallel.ai configuration status."""
    has_key = bool(settings.parallel_apikey)
    return f"""Parallel.ai Configuration:
- API Key: {"Configured ✓" if has_key else "Not configured ✗"}
- Base URL: {ParallelClient.BASE_URL}
- Beta Header: {ParallelClient.BETA_HEADER}

Available Tools:
- parallel_search: Web search with natural language
- parallel_extract: Extract content from URLs
- parallel_monitor_create: Create web monitors
- parallel_monitor_list: List all monitors
- parallel_monitor_delete: Delete a monitor
- parallel_task_run: Run tasks with processors
- parallel_task_status: Check task status
- parallel_findall: Entity discovery
- parallel_findall_result: Get FindAll results
"""


# === Main Entry Point ===


def main() -> None:
    """Run the MCP server."""
    import uvicorn

    uvicorn.run(
        "parallel_api.mcp_server:mcp_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
