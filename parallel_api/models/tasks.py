# ---
# entity_id: module-parallel-tasks
# entity_name: Tasks API Models
# entity_type_id: module
# entity_path: parallel_api/models/tasks.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [TaskRunRequest, TaskRun, TaskRunStatus, TaskSpec, TaskGroup]
# entity_dependencies: [pydantic]
# entity_callers: [parallel_api, clients]
# entity_callees: []
# entity_semver_impact: major
# entity_breaking_change_risk: medium
# entity_public_api: true
# ---

"""
Pydantic models for Parallel.ai Tasks API (v1 and Beta).

Task execution with processors, MCP servers, and webhooks.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TaskRunStatus(str, Enum):
    """Task run lifecycle status."""

    QUEUED = "queued"
    ACTION_REQUIRED = "action_required"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"


class SourcePolicy(BaseModel):
    """Source filtering policy for task web searches."""

    model_config = ConfigDict(extra="forbid")

    include_domains: list[str] | None = Field(
        default=None,
        description="Only include results from these domains",
    )
    exclude_domains: list[str] | None = Field(
        default=None,
        description="Exclude results from these domains",
    )


class MCPServerConfig(BaseModel):
    """Model Context Protocol server configuration."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(..., description="MCP server URL")
    name: str | None = Field(
        default=None,
        description="Server display name",
    )
    headers: dict[str, str] | None = Field(
        default=None,
        description="Custom headers for server requests",
    )


class TaskSpec(BaseModel):
    """Structured task specification with custom schemas."""

    model_config = ConfigDict(extra="allow")

    schema_: dict | None = Field(
        default=None,
        alias="schema",
        description="JSON schema for task output",
    )
    instructions: str | None = Field(
        default=None,
        description="Additional task instructions",
    )


class WebhookConfig(BaseModel):
    """Webhook configuration for task notifications."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(..., description="Webhook callback URL")
    headers: dict[str, str] | None = Field(
        default=None,
        description="Custom headers",
    )


class TaskRunRequest(BaseModel):
    """Request body for creating a task run."""

    model_config = ConfigDict(extra="forbid")

    processor: str = Field(
        ...,
        description="Processor selection for task execution",
    )
    input: str | dict[str, Any] = Field(
        ...,
        description="Task input—either text or JSON structure",
    )
    metadata: dict[str, str] | None = Field(
        default=None,
        description="User-provided key-value pairs (max 16 char keys, 512 char values)",
    )
    source_policy: SourcePolicy | None = Field(
        default=None,
        description="Domain preferences for web search results",
    )
    task_spec: TaskSpec | None = Field(
        default=None,
        description="Structured task specification",
    )
    mcp_servers: list[MCPServerConfig] | None = Field(
        default=None,
        description="Model Context Protocol servers for enhanced capabilities",
    )
    enable_events: bool | None = Field(
        default=None,
        description="Progress tracking toggle",
    )
    webhook: WebhookConfig | None = Field(
        default=None,
        description="Callback URL for run completion notifications",
    )


class TaskRunError(BaseModel):
    """Error details for failed task runs."""

    model_config = ConfigDict(extra="allow")

    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: dict | None = Field(
        default=None,
        description="Additional error details",
    )


class TaskRun(BaseModel):
    """Task run resource."""

    model_config = ConfigDict(extra="allow")

    run_id: str = Field(..., description="Unique task execution identifier")
    status: TaskRunStatus = Field(..., description="Current state")
    is_active: bool = Field(..., description="Whether run remains in active states")
    processor: str = Field(..., description="Processor used for execution")
    created_at: datetime = Field(..., description="Creation timestamp (RFC 3339)")
    modified_at: datetime = Field(..., description="Last modification timestamp")
    metadata: dict[str, str] | None = Field(
        default=None,
        description="Echoed user metadata",
    )
    taskgroup_id: str | None = Field(
        default=None,
        description="Associated batch group identifier",
    )
    warnings: list[dict] | None = Field(
        default=None,
        description="Non-fatal alerts",
    )
    error: TaskRunError | None = Field(
        default=None,
        description="Failure details when status is 'failed'",
    )


class TaskGroupRequest(BaseModel):
    """Request body for creating a task group."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(
        default=None,
        description="Group display name",
    )
    processor: str = Field(
        ...,
        description="Processor for all runs in group",
    )
    metadata: dict[str, str] | None = Field(
        default=None,
        description="Group metadata",
    )


class TaskGroup(BaseModel):
    """Task group resource for batch processing."""

    model_config = ConfigDict(extra="allow")

    taskgroup_id: str = Field(..., description="Unique group identifier")
    name: str | None = Field(default=None, description="Group name")
    processor: str = Field(..., description="Processor for group")
    status: str = Field(..., description="Group status")
    created_at: datetime = Field(..., description="Creation timestamp")
    run_count: int = Field(default=0, description="Number of runs in group")


class TaskGroupRun(BaseModel):
    """A run within a task group."""

    model_config = ConfigDict(extra="allow")

    run_id: str = Field(..., description="Run identifier")
    taskgroup_id: str = Field(..., description="Parent group identifier")
    status: TaskRunStatus = Field(..., description="Run status")
    input: str | dict[str, Any] = Field(..., description="Run input")
    created_at: datetime = Field(..., description="Creation timestamp")
