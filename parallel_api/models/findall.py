# ---
# entity_id: module-parallel-findall
# entity_name: FindAll API Models
# entity_type_id: module
# entity_path: parallel_api/models/findall.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [FindAllRequest, FindAllRun, FindAllStatus, FindAllGenerator]
# entity_dependencies: [pydantic]
# entity_callers: [parallel_api, clients]
# entity_callees: []
# entity_semver_impact: major
# entity_breaking_change_risk: medium
# entity_public_api: true
# ---

"""
Pydantic models for Parallel.ai FindAll API (Beta).

Entity discovery with matching conditions and enrichment.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FindAllGenerator(str, Enum):
    """FindAll processing tier."""

    BASE = "base"
    CORE = "core"
    PRO = "pro"
    PREVIEW = "preview"


class FindAllRunStatus(str, Enum):
    """FindAll run lifecycle status."""

    QUEUED = "queued"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MatchCondition(BaseModel):
    """Matching condition for entity discovery."""

    model_config = ConfigDict(extra="allow")

    field: str = Field(..., description="Field to match on")
    operator: str = Field(
        ...,
        description="Comparison operator (eq, contains, gt, lt, etc.)",
    )
    value: Any = Field(..., description="Value to match against")


class WebhookConfig(BaseModel):
    """Webhook configuration for FindAll notifications."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(..., description="Webhook callback URL")
    event_types: list[str] | None = Field(
        default=None,
        description="Event types to send",
    )


class FindAllRequest(BaseModel):
    """Request body for creating a FindAll run."""

    model_config = ConfigDict(extra="forbid")

    objective: str = Field(
        ...,
        description="Natural language objective",
        min_length=1,
    )
    entity_type: str = Field(
        ...,
        description="Entity classification (e.g., 'company', 'person')",
    )
    match_conditions: list[MatchCondition] = Field(
        ...,
        description="Matching criteria",
        min_length=1,
    )
    generator: FindAllGenerator = Field(
        ...,
        description="Processing tier",
    )
    match_limit: int = Field(
        ...,
        ge=5,
        le=1000,
        description="Results cap (5-1000 inclusive)",
    )
    exclude_list: list[str] | None = Field(
        default=None,
        description="Entities to skip",
    )
    metadata: dict[str, str] | None = Field(
        default=None,
        description="Custom tracking data",
    )
    webhook: WebhookConfig | None = Field(
        default=None,
        description="Event notifications",
    )


class FindAllStatusMetrics(BaseModel):
    """Progress metrics for FindAll run."""

    model_config = ConfigDict(extra="allow")

    matches_found: int = Field(default=0, description="Number of matches found")
    pages_searched: int = Field(default=0, description="Pages searched")
    enrichments_completed: int = Field(default=0, description="Enrichments done")


class FindAllStatus(BaseModel):
    """Status object for FindAll run."""

    model_config = ConfigDict(extra="allow")

    status: FindAllRunStatus = Field(..., description="Run state")
    is_active: bool = Field(..., description="Execution state")
    metrics: FindAllStatusMetrics | None = Field(
        default=None,
        description="Progress tracking",
    )


class FindAllRun(BaseModel):
    """FindAll run resource."""

    model_config = ConfigDict(extra="allow")

    findall_id: str = Field(..., description="Unique run identifier")
    status: FindAllStatus = Field(..., description="Current state information")
    generator: FindAllGenerator = Field(..., description="Selected processor tier")
    metadata: dict[str, str] | None = Field(
        default=None,
        description="User-provided context",
    )
    created_at: datetime = Field(..., description="Creation timestamp (RFC 3339)")
    modified_at: datetime = Field(..., description="Last update timestamp")


class EnrichmentRequest(BaseModel):
    """Request body for adding enrichment to FindAll run."""

    model_config = ConfigDict(extra="forbid")

    enrichment_type: str = Field(
        ...,
        description="Type of enrichment to add",
    )
    fields: list[str] = Field(
        ...,
        description="Fields to enrich",
        min_length=1,
    )
    options: dict[str, Any] | None = Field(
        default=None,
        description="Enrichment options",
    )


class FindAllMatch(BaseModel):
    """A single match from FindAll run."""

    model_config = ConfigDict(extra="allow")

    entity_id: str = Field(..., description="Matched entity ID")
    entity_type: str = Field(..., description="Entity type")
    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Entity data",
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Match confidence score",
    )
    source_url: str | None = Field(
        default=None,
        description="Source URL for match",
    )


class FindAllResult(BaseModel):
    """Complete result from FindAll run."""

    model_config = ConfigDict(extra="allow")

    findall_id: str = Field(..., description="Run identifier")
    matches: list[FindAllMatch] = Field(
        default_factory=list,
        description="Found matches",
    )
    total_matches: int = Field(default=0, description="Total match count")
    schema: dict | None = Field(
        default=None,
        description="Result schema",
    )
