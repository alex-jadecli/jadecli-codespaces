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

import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.settings import settings
from parallel_api.clients.async_client import ParallelClient

# === Error Models ===


class ErrorInfo(BaseModel):
    """Structured error response per Anthropic error handling patterns."""

    type: str  # "invalid_request_error", "authentication_error", etc.
    message: str  # Human-readable error message
    param: str | None = None  # Parameter that caused the error
    code: str | None = None  # Machine-readable error code


class APIException(HTTPException):
    """Extended HTTPException with structured error fields."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        param: str | None = None,
        code: str | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.param = param
        self.code = code


def _status_to_error_type(status_code: int) -> str:
    """Map HTTP status codes to Anthropic-style error types."""
    return {
        400: "invalid_request_error",
        401: "authentication_error",
        403: "permission_error",
        404: "not_found_error",
        422: "invalid_request_error",
        429: "rate_limit_error",
        500: "api_error",
        502: "api_error",
        503: "overloaded_error",
    }.get(status_code, "api_error")


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


# === Exception Handlers ===


@app.exception_handler(HTTPException)
async def structured_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    """Convert HTTPException to structured error response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": _status_to_error_type(exc.status_code),
                "message": exc.detail,
                "param": getattr(exc, "param", None),
                "code": getattr(exc, "code", None),
            }
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Convert unhandled exceptions to structured error response."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "api_error",
                "message": str(exc),
                "param": None,
                "code": "internal_error",
            }
        },
    )


# === Dependencies ===


async def get_parallel_client() -> ParallelClient:
    """Dependency to get configured Parallel client."""
    if not settings.parallel_apikey:
        raise APIException(
            status_code=500,
            detail="PARALLEL_APIKEY not configured. Set environment variable or add to .env file.",
            code="missing_api_key",
        )
    return ParallelClient(api_key=settings.parallel_apikey)


# === Request/Response Models ===


class SearchRequestBody(BaseModel):
    """Simplified search request."""

    objective: str | None = None
    search_queries: list[str] | None = None
    max_results: int = Field(default=10, ge=1, le=100)
    mode: str = Field(default="one-shot")


class ExtractRequestBody(BaseModel):
    """Simplified extract request."""

    urls: list[str] = Field(..., min_length=1)
    objective: str | None = None
    full_content: bool = False


class MonitorCreateBody(BaseModel):
    """Monitor creation request."""

    query: str
    cadence: str = Field(default="daily")
    webhook_url: str | None = None


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
        raise APIException(
            status_code=500,
            detail=f"Search operation failed: {e}",
            code="search_failed",
        )


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
        raise APIException(
            status_code=500,
            detail=f"Content extraction failed: {e}",
            code="extract_failed",
        )


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
        raise APIException(
            status_code=500,
            detail=f"Failed to list monitors: {e}",
            code="list_monitors_failed",
        )


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
        raise APIException(
            status_code=500,
            detail=f"Failed to create monitor: {e}",
            code="create_monitor_failed",
        )


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
        raise APIException(
            status_code=404,
            detail=f"Monitor not found or retrieval failed: {e}",
            param="monitor_id",
            code="monitor_not_found",
        )


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
        raise APIException(
            status_code=500,
            detail=f"Failed to delete monitor: {e}",
            param="monitor_id",
            code="delete_monitor_failed",
        )


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
        raise APIException(
            status_code=500,
            detail=f"Failed to create task: {e}",
            code="create_task_failed",
        )


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
        raise APIException(
            status_code=404,
            detail=f"Task not found or retrieval failed: {e}",
            param="run_id",
            code="task_not_found",
        )


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
        raise APIException(
            status_code=500,
            detail=f"Failed to create FindAll run: {e}",
            code="create_findall_failed",
        )


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
        raise APIException(
            status_code=404,
            detail=f"FindAll run not found or retrieval failed: {e}",
            param="findall_id",
            code="findall_not_found",
        )


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
        raise APIException(
            status_code=404,
            detail=f"FindAll result not found or retrieval failed: {e}",
            param="findall_id",
            code="findall_result_not_found",
        )


# === Task Dispatch Endpoints (jade-dev-assist integration) ===


class TaskDispatchBody(BaseModel):
    """Task dispatch request for worker agents."""

    task_id: str | None = None
    project: str
    task_description: str
    priority: int = Field(default=1, ge=1, le=5)
    max_turns: int = Field(default=25, ge=1, le=50)


class TaskStatusResponse(BaseModel):
    """Task status response."""

    task_id: str
    status: str  # pending, running, completed, failed, cancelled
    project: str
    created_at: str
    started_at: str | None = None
    completed_at: str | None = None
    result: dict[str, Any] | None = None
    error: str | None = None


# In-memory task store (replace with database later)
_task_store: dict[str, dict[str, Any]] = {}


@app.post("/tasks/dispatch", response_model=TaskStatusResponse)
async def dispatch_task(body: TaskDispatchBody) -> TaskStatusResponse:
    """
    Dispatch a task to a worker agent.

    This endpoint creates a task for execution by a jade-dev-assist worker.
    The task will be queued and executed asynchronously.
    """
    import uuid
    from datetime import UTC, datetime

    task_id = body.task_id or str(uuid.uuid4())

    # Create task record
    task = {
        "task_id": task_id,
        "status": "pending",
        "project": body.project,
        "task_description": body.task_description,
        "priority": body.priority,
        "max_turns": body.max_turns,
        "created_at": datetime.now(UTC).isoformat(),
        "started_at": None,
        "completed_at": None,
        "result": None,
        "error": None,
    }

    _task_store[task_id] = task

    return TaskStatusResponse(**task)


@app.get("/tasks/{task_id}/status", response_model=TaskStatusResponse)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """
    Get the status of a dispatched task.

    Returns current status and results if completed.
    """
    task = _task_store.get(task_id)

    if not task:
        raise APIException(
            status_code=404,
            detail=f"Task not found: {task_id}",
            param="task_id",
            code="task_not_found",
        )

    return TaskStatusResponse(**task)


@app.post("/tasks/{task_id}/cancel")
async def cancel_task(task_id: str) -> dict[str, Any]:
    """
    Cancel a running task.

    This will attempt to gracefully stop the worker agent.
    """
    task = _task_store.get(task_id)

    if not task:
        raise APIException(
            status_code=404,
            detail=f"Task not found: {task_id}",
            param="task_id",
            code="task_not_found",
        )

    if task["status"] in ("completed", "failed", "cancelled"):
        raise APIException(
            status_code=400,
            detail=f"Cannot cancel task in {task['status']} state",
            param="task_id",
            code="invalid_task_state",
        )

    task["status"] = "cancelled"

    from datetime import UTC, datetime

    task["completed_at"] = datetime.now(UTC).isoformat()

    return {"cancelled": True, "task_id": task_id, "status": task["status"]}


# === Main Entry Point ===


def main() -> None:
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
