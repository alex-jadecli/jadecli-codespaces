# ---
# entity_id: module-parallel-fastapi
# entity_name: Parallel.ai FastAPI Application
# entity_type_id: module
# entity_path: parallel_api/fastapi_app.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [app, router]
# entity_dependencies: [fastapi, clients, models, settings]
# entity_callers: [uvicorn]
# entity_callees: [clients]
# entity_semver_impact: minor
# entity_breaking_change_risk: medium
# entity_public_api: true
# entity_actors: [dev, user]
# ---

"""
FastAPI Application for Parallel.ai API proxy.

Provides REST endpoints that proxy to Parallel.ai:
- POST /api/search - Web search
- POST /api/extract - Content extraction
- GET/POST/DELETE /api/monitors - Monitor CRUD
- POST /api/tasks - Task execution
- POST /api/findall - Entity discovery

Usage:
    uvicorn parallel_api.fastapi_app:app --reload

    # Or via CLI
    python -m parallel_api.fastapi_app

Configuration:
    Requires PARALLEL_APIKEY in .env or environment.
"""

from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.settings import settings
from parallel_api.clients.async_client import ParallelClient
from parallel_api.models import (
    SearchRequest,
    SearchResponse,
    ExtractRequest,
    ExtractResponse,
    CreateMonitorRequest,
    Monitor,
    TaskRunRequest,
    TaskRun,
    FindAllRequest,
    FindAllRun,
)


# === Lifespan ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    if not settings.parallel_apikey:
        print("WARNING: PARALLEL_APIKEY not configured")
    yield
    # Shutdown


# === FastAPI App ===

app = FastAPI(
    title="Parallel.ai API Proxy",
    description="FastAPI proxy for Parallel.ai web intelligence APIs",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Dependencies ===

async def get_parallel_client() -> ParallelClient:
    """Dependency to get configured Parallel client."""
    if not settings.parallel_apikey:
        raise HTTPException(
            status_code=500,
            detail="PARALLEL_APIKEY not configured",
        )
    return ParallelClient(api_key=settings.parallel_apikey)


# === Request/Response Models ===

class SearchRequestBody(BaseModel):
    """Simplified search request."""
    objective: Optional[str] = None
    search_queries: Optional[list[str]] = None
    max_results: int = Field(default=10, ge=1, le=100)
    mode: str = Field(default="one-shot")


class ExtractRequestBody(BaseModel):
    """Simplified extract request."""
    urls: list[str] = Field(..., min_length=1)
    objective: Optional[str] = None
    full_content: bool = False


class MonitorCreateBody(BaseModel):
    """Monitor creation request."""
    query: str
    cadence: str = Field(default="daily")
    webhook_url: Optional[str] = None


class TaskRunBody(BaseModel):
    """Task run request."""
    processor: str
    input: str
    wait_for_completion: bool = True


class FindAllBody(BaseModel):
    """FindAll request."""
    objective: str
    entity_type: str
    match_limit: int = Field(default=50, ge=5, le=1000)
    generator: str = Field(default="core")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    parallel_api_configured: bool
    version: str


# === Health Check ===

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        parallel_api_configured=bool(settings.parallel_apikey),
        version="0.1.0",
    )


# === Search Endpoints ===

@app.post("/api/search")
async def search(
    body: SearchRequestBody,
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """
    Perform web search using Parallel.ai.

    Returns search results with URLs, titles, and excerpts.
    """
    try:
        async with client:
            response = await client.search(
                objective=body.objective,
                search_queries=body.search_queries,
                max_results=body.max_results,
                mode=body.mode,
            )

        return {
            "search_id": response.search_id,
            "results": [r.model_dump() for r in response.results],
            "result_count": len(response.results),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Extract Endpoints ===

@app.post("/api/extract")
async def extract(
    body: ExtractRequestBody,
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """
    Extract content from URLs using Parallel.ai.

    Returns extracted content with titles and excerpts.
    """
    try:
        async with client:
            response = await client.extract(
                urls=body.urls,
                objective=body.objective,
                full_content=body.full_content,
            )

        return {
            "extract_id": response.extract_id,
            "results": [r.model_dump() for r in response.results],
            "errors": [e.model_dump() for e in response.errors],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Monitor Endpoints ===

@app.get("/api/monitors")
async def list_monitors(
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """List all monitors."""
    try:
        async with client:
            monitors = await client.list_monitors()

        return {
            "monitors": [m.model_dump() for m in monitors],
            "count": len(monitors),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/monitors")
async def create_monitor(
    body: MonitorCreateBody,
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """Create a new monitor."""
    try:
        async with client:
            monitor = await client.create_monitor(
                query=body.query,
                cadence=body.cadence,
                webhook_url=body.webhook_url,
            )

        return monitor.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/monitors/{monitor_id}")
async def get_monitor(
    monitor_id: str,
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """Get a monitor by ID."""
    try:
        async with client:
            monitor = await client.get_monitor(monitor_id)

        return monitor.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/monitors/{monitor_id}")
async def delete_monitor(
    monitor_id: str,
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """Delete a monitor."""
    try:
        async with client:
            await client.delete_monitor(monitor_id)

        return {"deleted": True, "monitor_id": monitor_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Task Endpoints ===

@app.post("/api/tasks")
async def create_task(
    body: TaskRunBody,
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """Create and optionally wait for a task run."""
    try:
        async with client:
            run = await client.create_task_run(
                processor=body.processor,
                input=body.input,
            )

            if body.wait_for_completion:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks/{run_id}")
async def get_task(
    run_id: str,
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """Get task run status."""
    try:
        async with client:
            run = await client.get_task_run(run_id)

            response = run.model_dump()

            if run.status.value == "completed":
                result = await client.get_task_run_result(run_id)
                response["result"] = result

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === FindAll Endpoints ===

@app.post("/api/findall")
async def create_findall(
    body: FindAllBody,
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """Create a FindAll run for entity discovery."""
    try:
        async with client:
            run = await client.create_findall_run(
                objective=body.objective,
                entity_type=body.entity_type,
                match_conditions=[{"field": "name", "operator": "exists", "value": True}],
                generator=body.generator,
                match_limit=body.match_limit,
            )

        return {
            "findall_id": run.findall_id,
            "status": run.status.status.value,
            "is_active": run.status.is_active,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/findall/{findall_id}")
async def get_findall(
    findall_id: str,
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """Get FindAll run status."""
    try:
        async with client:
            run = await client.get_findall_run(findall_id)

        return {
            "findall_id": run.findall_id,
            "status": run.status.status.value,
            "is_active": run.status.is_active,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/findall/{findall_id}/result")
async def get_findall_result(
    findall_id: str,
    client: ParallelClient = Depends(get_parallel_client),
) -> dict[str, Any]:
    """Get FindAll run results."""
    try:
        async with client:
            result = await client.get_findall_result(findall_id)

        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Main Entry Point ===

def main():
    """Run the FastAPI server."""
    import uvicorn
    uvicorn.run(
        "parallel_api.fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
