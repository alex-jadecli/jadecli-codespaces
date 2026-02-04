# ---
# entity_id: module-parallel-async-client
# entity_name: Parallel.ai Async Client
# entity_type_id: module
# entity_path: parallel_api/clients/async_client.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [ParallelClient]
# entity_dependencies: [httpx, models]
# entity_callers: [parallel_api, mcp_server, cli]
# entity_callees: [models]
# entity_semver_impact: major
# entity_breaking_change_risk: high
# entity_public_api: true
# entity_actors: [dev, claude]
# ---

"""
Async HTTP client for Parallel.ai API.

Provides async methods for all Parallel.ai endpoints:
- Extract (Beta)
- Search (Beta)
- Monitor (CRUD)
- Tasks v1 / Beta
- FindAll (Beta)

Usage:
    from parallel_api.clients import ParallelClient
    from cli.settings import settings

    async with ParallelClient(api_key=settings.parallel_apikey) as client:
        results = await client.search(objective="Find AI companies")
"""

import asyncio
from typing import Any

import httpx

from parallel_api.models.extract import ExtractRequest, ExtractResponse
from parallel_api.models.findall import (
    EnrichmentRequest,
    FindAllRequest,
    FindAllResult,
    FindAllRun,
)
from parallel_api.models.monitor import (
    CreateMonitorRequest,
    Monitor,
    MonitorEvent,
    UpdateMonitorRequest,
)
from parallel_api.models.search import SearchRequest, SearchResponse
from parallel_api.models.tasks import (
    TaskGroup,
    TaskGroupRequest,
    TaskRun,
    TaskRunRequest,
)


class ParallelClient:
    """
    Async HTTP client for Parallel.ai API.

    All methods are async and support context manager pattern.
    Uses httpx for async HTTP requests with connection pooling.
    """

    BASE_URL = "https://api.parallel.ai"
    BETA_HEADER = "search-extract-2025-10-10"

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        """
        Initialize Parallel.ai client.

        Args:
            api_key: Parallel.ai API key
            base_url: Override base URL (for testing)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "ParallelClient":
        """Enter async context manager."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client, raising if not in context."""
        if self._client is None:
            raise RuntimeError(
                "ParallelClient must be used as async context manager: "
                "async with ParallelClient(...) as client:"
            )
        return self._client

    def _beta_headers(self) -> dict[str, str]:
        """Get headers for beta endpoints."""
        return {"parallel-beta": self.BETA_HEADER}

    # === Extract API ===

    async def extract(
        self,
        urls: list[str],
        objective: str | None = None,
        search_queries: list[str] | None = None,
        excerpts: bool = True,
        full_content: bool = False,
    ) -> ExtractResponse:
        """
        Extract content from web URLs.

        Args:
            urls: Web URLs to extract content from
            objective: Focus extraction on this objective
            search_queries: Focus extraction on these keywords
            excerpts: Include relevant excerpts
            full_content: Include complete content

        Returns:
            ExtractResponse with results and any errors
        """
        request = ExtractRequest(
            urls=urls,
            objective=objective,
            search_queries=search_queries,
            excerpts=excerpts,
            full_content=full_content,
        )

        response = await self.client.post(
            "/v1beta/extract",
            json=request.model_dump(exclude_none=True),
            headers=self._beta_headers(),
        )
        response.raise_for_status()
        return ExtractResponse.model_validate(response.json())

    # === Search API ===

    async def search(
        self,
        objective: str | None = None,
        search_queries: list[str] | None = None,
        max_results: int = 10,
        mode: str = "one-shot",
    ) -> SearchResponse:
        """
        Perform web search.

        Args:
            objective: Natural-language search objective
            search_queries: Keyword search queries
            max_results: Maximum results to return
            mode: Search mode (one-shot or agentic)

        Returns:
            SearchResponse with results
        """
        request = SearchRequest(
            objective=objective,
            search_queries=search_queries,
            max_results=max_results,
            mode=mode,
        )

        response = await self.client.post(
            "/v1beta/search",
            json=request.model_dump(exclude_none=True),
            headers=self._beta_headers(),
        )
        response.raise_for_status()
        return SearchResponse.model_validate(response.json())

    # === Monitor API ===

    async def list_monitors(self) -> list[Monitor]:
        """List all monitors."""
        response = await self.client.get("/v1alpha/monitors")
        response.raise_for_status()
        data = response.json()
        return [Monitor.model_validate(m) for m in data.get("monitors", [])]

    async def create_monitor(
        self,
        query: str,
        cadence: str,
        metadata: dict[str, str] | None = None,
        webhook_url: str | None = None,
    ) -> Monitor:
        """
        Create a new monitor.

        Args:
            query: Query to monitor
            cadence: Execution cadence (hourly, daily, weekly)
            metadata: Custom metadata
            webhook_url: Webhook callback URL

        Returns:
            Created Monitor
        """
        request = CreateMonitorRequest(
            query=query,
            cadence=cadence,
            metadata=metadata,
            webhook={"url": webhook_url} if webhook_url else None,
        )

        response = await self.client.post(
            "/v1alpha/monitors",
            json=request.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return Monitor.model_validate(response.json())

    async def get_monitor(self, monitor_id: str) -> Monitor:
        """Retrieve a monitor by ID."""
        response = await self.client.get(f"/v1alpha/monitors/{monitor_id}")
        response.raise_for_status()
        return Monitor.model_validate(response.json())

    async def update_monitor(
        self,
        monitor_id: str,
        query: str | None = None,
        cadence: str | None = None,
        status: str | None = None,
    ) -> Monitor:
        """Update a monitor."""
        request = UpdateMonitorRequest(
            query=query,
            cadence=cadence,
            status=status,
        )

        response = await self.client.post(
            f"/v1alpha/monitors/{monitor_id}",
            json=request.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return Monitor.model_validate(response.json())

    async def delete_monitor(self, monitor_id: str) -> None:
        """Delete a monitor."""
        response = await self.client.delete(f"/v1alpha/monitors/{monitor_id}")
        response.raise_for_status()

    async def list_monitor_events(self, monitor_id: str) -> list[MonitorEvent]:
        """List events for a monitor."""
        response = await self.client.get(f"/v1alpha/monitors/{monitor_id}/events")
        response.raise_for_status()
        data = response.json()
        return [MonitorEvent.model_validate(e) for e in data.get("events", [])]

    # === Tasks v1 API ===

    async def create_task_run(
        self,
        processor: str,
        input: str | dict[str, Any],
        metadata: dict[str, str] | None = None,
        enable_events: bool = True,
    ) -> TaskRun:
        """
        Create a new task run.

        Args:
            processor: Processor to use
            input: Task input (text or structured)
            metadata: Custom metadata
            enable_events: Enable progress events

        Returns:
            Created TaskRun (status: queued)
        """
        request = TaskRunRequest(
            processor=processor,
            input=input,
            metadata=metadata,
            enable_events=enable_events,
        )

        response = await self.client.post(
            "/v1/tasks/runs",
            json=request.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        return TaskRun.model_validate(response.json())

    async def get_task_run(self, run_id: str) -> TaskRun:
        """Retrieve a task run by ID."""
        response = await self.client.get(f"/v1/tasks/runs/{run_id}")
        response.raise_for_status()
        return TaskRun.model_validate(response.json())

    async def get_task_run_result(self, run_id: str) -> dict[str, Any]:
        """Retrieve the result of a completed task run."""
        response = await self.client.get(f"/v1/tasks/runs/{run_id}/result")
        response.raise_for_status()
        return response.json()

    async def wait_for_task_run(
        self,
        run_id: str,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> TaskRun:
        """
        Wait for a task run to complete.

        Args:
            run_id: Task run ID
            poll_interval: Seconds between status checks
            timeout: Maximum wait time

        Returns:
            Completed TaskRun

        Raises:
            TimeoutError: If task doesn't complete in time
        """
        import time

        start = time.time()

        while True:
            run = await self.get_task_run(run_id)
            if not run.is_active:
                return run

            if time.time() - start > timeout:
                raise TimeoutError(f"Task {run_id} did not complete within {timeout}s")

            await asyncio.sleep(poll_interval)

    # === Tasks Beta API ===

    async def create_task_group(
        self,
        processor: str,
        name: str | None = None,
    ) -> TaskGroup:
        """Create a task group for batch processing."""
        request = TaskGroupRequest(
            processor=processor,
            name=name,
        )

        response = await self.client.post(
            "/v1beta/tasks/groups",
            json=request.model_dump(exclude_none=True),
            headers=self._beta_headers(),
        )
        response.raise_for_status()
        return TaskGroup.model_validate(response.json())

    async def get_task_group(self, taskgroup_id: str) -> TaskGroup:
        """Retrieve a task group by ID."""
        response = await self.client.get(
            f"/v1beta/tasks/groups/{taskgroup_id}",
            headers=self._beta_headers(),
        )
        response.raise_for_status()
        return TaskGroup.model_validate(response.json())

    # === FindAll API ===

    async def create_findall_run(
        self,
        objective: str,
        entity_type: str,
        match_conditions: list[dict[str, Any]],
        generator: str = "core",
        match_limit: int = 100,
    ) -> FindAllRun:
        """
        Create a FindAll run for entity discovery.

        Args:
            objective: Natural language objective
            entity_type: Entity classification
            match_conditions: Matching criteria
            generator: Processing tier (base, core, pro, preview)
            match_limit: Maximum matches (5-1000)

        Returns:
            Created FindAllRun
        """
        request = FindAllRequest(
            objective=objective,
            entity_type=entity_type,
            match_conditions=match_conditions,
            generator=generator,
            match_limit=match_limit,
        )

        response = await self.client.post(
            "/v1beta/findall/runs",
            json=request.model_dump(exclude_none=True),
            headers=self._beta_headers(),
        )
        response.raise_for_status()
        return FindAllRun.model_validate(response.json())

    async def get_findall_run(self, findall_id: str) -> FindAllRun:
        """Retrieve a FindAll run by ID."""
        response = await self.client.get(
            f"/v1beta/findall/runs/{findall_id}",
            headers=self._beta_headers(),
        )
        response.raise_for_status()
        return FindAllRun.model_validate(response.json())

    async def get_findall_result(self, findall_id: str) -> FindAllResult:
        """Retrieve the result of a FindAll run."""
        response = await self.client.get(
            f"/v1beta/findall/runs/{findall_id}/result",
            headers=self._beta_headers(),
        )
        response.raise_for_status()
        return FindAllResult.model_validate(response.json())

    async def cancel_findall_run(self, findall_id: str) -> FindAllRun:
        """Cancel a FindAll run."""
        response = await self.client.post(
            f"/v1beta/findall/runs/{findall_id}/cancel",
            headers=self._beta_headers(),
        )
        response.raise_for_status()
        return FindAllRun.model_validate(response.json())

    async def extend_findall_run(
        self,
        findall_id: str,
        additional_matches: int = 50,
    ) -> FindAllRun:
        """Extend a FindAll run with more matches."""
        response = await self.client.post(
            f"/v1beta/findall/runs/{findall_id}/extend",
            json={"additional_matches": additional_matches},
            headers=self._beta_headers(),
        )
        response.raise_for_status()
        return FindAllRun.model_validate(response.json())

    async def add_findall_enrichment(
        self,
        findall_id: str,
        enrichment_type: str,
        fields: list[str],
    ) -> FindAllRun:
        """Add enrichment to a FindAll run."""
        request = EnrichmentRequest(
            enrichment_type=enrichment_type,
            fields=fields,
        )

        response = await self.client.post(
            f"/v1beta/findall/runs/{findall_id}/enrich",
            json=request.model_dump(exclude_none=True),
            headers=self._beta_headers(),
        )
        response.raise_for_status()
        return FindAllRun.model_validate(response.json())
