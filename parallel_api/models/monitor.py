# ---
# entity_id: module-parallel-monitor
# entity_name: Monitor API Models
# entity_type_id: module
# entity_path: parallel_api/models/monitor.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [Monitor, CreateMonitorRequest, MonitorStatus, MonitorCadence]
# entity_dependencies: [pydantic]
# entity_callers: [parallel_api, clients]
# entity_callees: []
# entity_semver_impact: major
# entity_breaking_change_risk: medium
# entity_public_api: true
# ---

"""
Pydantic models for Parallel.ai Monitor API.

Continuous web monitoring with scheduled queries and webhook notifications.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class MonitorStatus(str, Enum):
    """Monitor lifecycle status."""

    ACTIVE = "active"
    CANCELED = "canceled"


class MonitorCadence(str, Enum):
    """Monitor execution cadence."""

    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"


class WebhookEventType(str, Enum):
    """Webhook event types."""

    NEW_RESULT = "new_result"
    RUN_COMPLETED = "run_completed"
    ERROR = "error"


class WebhookConfig(BaseModel):
    """Webhook configuration for monitor notifications."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(..., description="Webhook callback URL")
    event_types: Optional[list[WebhookEventType]] = Field(
        default=None,
        description="Event types to send to webhook",
    )
    headers: Optional[dict[str, str]] = Field(
        default=None,
        description="Custom headers for webhook requests",
    )


class CreateMonitorRequest(BaseModel):
    """Request body for creating a monitor."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(
        ...,
        description="The query to monitor",
        min_length=1,
    )
    cadence: MonitorCadence = Field(
        ...,
        description="Execution cadence",
    )
    metadata: Optional[dict[str, str]] = Field(
        default=None,
        description="User-provided custom metadata",
    )
    webhook: Optional[WebhookConfig] = Field(
        default=None,
        description="Webhook configuration for notifications",
    )


class UpdateMonitorRequest(BaseModel):
    """Request body for updating a monitor."""

    model_config = ConfigDict(extra="forbid")

    query: Optional[str] = Field(
        default=None,
        description="Updated query",
    )
    cadence: Optional[MonitorCadence] = Field(
        default=None,
        description="Updated cadence",
    )
    status: Optional[MonitorStatus] = Field(
        default=None,
        description="Updated status",
    )
    metadata: Optional[dict[str, str]] = Field(
        default=None,
        description="Updated metadata",
    )
    webhook: Optional[WebhookConfig] = Field(
        default=None,
        description="Updated webhook config",
    )


class Monitor(BaseModel):
    """Monitor resource."""

    model_config = ConfigDict(extra="allow")

    monitor_id: str = Field(..., description="Unique monitor identifier")
    query: str = Field(..., description="The monitored query")
    status: MonitorStatus = Field(..., description="Current status")
    cadence: MonitorCadence = Field(..., description="Execution cadence")
    metadata: Optional[dict[str, str]] = Field(
        default=None,
        description="User-provided metadata",
    )
    webhook: Optional[WebhookConfig] = Field(
        default=None,
        description="Webhook configuration",
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    last_run_at: Optional[datetime] = Field(
        default=None,
        description="Most recent execution timestamp",
    )


class MonitorEvent(BaseModel):
    """A single monitor event."""

    model_config = ConfigDict(extra="allow")

    event_id: str = Field(..., description="Unique event ID")
    event_type: str = Field(..., description="Type of event")
    created_at: datetime = Field(..., description="Event timestamp")
    data: Optional[dict] = Field(
        default=None,
        description="Event data",
    )


class EventGroup(BaseModel):
    """Group of related monitor events."""

    model_config = ConfigDict(extra="allow")

    event_group_id: str = Field(..., description="Unique event group ID")
    monitor_id: str = Field(..., description="Associated monitor ID")
    events: list[MonitorEvent] = Field(
        default_factory=list,
        description="Events in this group",
    )
    created_at: datetime = Field(..., description="Group creation timestamp")
