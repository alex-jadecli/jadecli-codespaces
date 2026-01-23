# ---
# entity_id: module-parallel-models
# entity_name: Parallel.ai API Models
# entity_type_id: module
# entity_path: parallel_api/models/__init__.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [ExtractRequest, SearchRequest, Monitor, TaskRun, FindAllRun]
# entity_dependencies: [extract, search, monitor, tasks, findall]
# entity_callers: [parallel_api, clients]
# entity_callees: []
# entity_semver_impact: major
# entity_breaking_change_risk: high
# entity_public_api: true
# ---

"""
Pydantic models for Parallel.ai API schemas.

All request and response models for:
- Extract (Beta)
- Search (Beta)
- Monitor
- Tasks v1 / Tasks Beta
- FindAll (Beta)
"""

from parallel_api.models.extract import (
    ExtractRequest,
    ExtractResponse,
    ExtractResult,
    ExtractError,
    FetchPolicy,
    ExcerptSettings,
    FullContentSettings,
)

from parallel_api.models.search import (
    SearchRequest,
    SearchResponse,
    SearchResult,
    SearchMode,
    SourcePolicy,
    ExcerptConfig,
)

from parallel_api.models.monitor import (
    Monitor,
    MonitorStatus,
    MonitorCadence,
    CreateMonitorRequest,
    UpdateMonitorRequest,
    WebhookConfig,
    MonitorEvent,
    EventGroup,
)

from parallel_api.models.tasks import (
    TaskRunRequest,
    TaskRun,
    TaskRunStatus,
    TaskSpec,
    MCPServerConfig,
    TaskGroup,
    TaskGroupRun,
)

from parallel_api.models.findall import (
    FindAllRequest,
    FindAllRun,
    FindAllStatus,
    FindAllGenerator,
    MatchCondition,
    EnrichmentRequest,
    FindAllResult,
)

__all__ = [
    # Extract
    "ExtractRequest",
    "ExtractResponse",
    "ExtractResult",
    "ExtractError",
    "FetchPolicy",
    "ExcerptSettings",
    "FullContentSettings",
    # Search
    "SearchRequest",
    "SearchResponse",
    "SearchResult",
    "SearchMode",
    "SourcePolicy",
    "ExcerptConfig",
    # Monitor
    "Monitor",
    "MonitorStatus",
    "MonitorCadence",
    "CreateMonitorRequest",
    "UpdateMonitorRequest",
    "WebhookConfig",
    "MonitorEvent",
    "EventGroup",
    # Tasks
    "TaskRunRequest",
    "TaskRun",
    "TaskRunStatus",
    "TaskSpec",
    "MCPServerConfig",
    "TaskGroup",
    "TaskGroupRun",
    # FindAll
    "FindAllRequest",
    "FindAllRun",
    "FindAllStatus",
    "FindAllGenerator",
    "MatchCondition",
    "EnrichmentRequest",
    "FindAllResult",
]
