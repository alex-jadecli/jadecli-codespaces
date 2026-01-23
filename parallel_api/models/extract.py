# ---
# entity_id: module-parallel-extract
# entity_name: Extract API Models
# entity_type_id: module
# entity_path: parallel_api/models/extract.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [ExtractRequest, ExtractResponse, ExtractResult, ExtractError]
# entity_dependencies: [pydantic]
# entity_callers: [parallel_api, clients]
# entity_callees: []
# entity_semver_impact: major
# entity_breaking_change_risk: medium
# entity_public_api: true
# ---

"""
Pydantic models for Parallel.ai Extract API (Beta).

POST /v1beta/extract
Extract content from web URLs with optional focusing on objectives/queries.
"""

from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class FetchPolicy(BaseModel):
    """Controls cached vs. live content retrieval."""

    model_config = ConfigDict(extra="forbid")

    max_age_seconds: Optional[int] = Field(
        default=None,
        description="Maximum age of cached content in seconds",
    )
    timeout_seconds: Optional[int] = Field(
        default=None,
        description="Request timeout in seconds",
    )
    disable_cache_fallback: Optional[bool] = Field(
        default=None,
        description="Disable fallback to cached content on failure",
    )


class ExcerptSettings(BaseModel):
    """Settings for excerpt extraction."""

    model_config = ConfigDict(extra="forbid")

    max_chars_per_result: Optional[int] = Field(
        default=None,
        description="Maximum characters per excerpt",
    )
    max_chars_total: Optional[int] = Field(
        default=None,
        description="Maximum total characters across all excerpts",
    )


class FullContentSettings(BaseModel):
    """Settings for full content extraction."""

    model_config = ConfigDict(extra="forbid")

    max_chars: Optional[int] = Field(
        default=None,
        description="Maximum characters to extract",
    )


class ExtractRequest(BaseModel):
    """Request body for Extract API."""

    model_config = ConfigDict(extra="forbid")

    urls: list[str] = Field(
        ...,
        description="Web URLs to extract content from",
        min_length=1,
    )
    objective: Optional[str] = Field(
        default=None,
        description="Focuses extracted content on the specified search objective",
    )
    search_queries: Optional[list[str]] = Field(
        default=None,
        description="Focuses extracted content on the specified keyword search queries",
    )
    fetch_policy: Optional[FetchPolicy] = Field(
        default=None,
        description="Determines cached vs. live content retrieval",
    )
    excerpts: Union[bool, ExcerptSettings] = Field(
        default=True,
        description="Include relevant excerpts from each URL",
    )
    full_content: Union[bool, FullContentSettings] = Field(
        default=False,
        description="Include complete content from each URL",
    )


class ExtractResult(BaseModel):
    """Successful extraction result for a single URL."""

    model_config = ConfigDict(extra="allow")

    url: str = Field(..., description="The extracted URL")
    title: Optional[str] = Field(default=None, description="Page title")
    excerpts: Optional[list[str]] = Field(
        default=None,
        description="Relevant excerpts from the page",
    )
    full_content: Optional[str] = Field(
        default=None,
        description="Complete page content",
    )


class ExtractError(BaseModel):
    """Error result for a failed URL extraction."""

    model_config = ConfigDict(extra="allow")

    url: str = Field(..., description="The failed URL")
    error_type: str = Field(..., description="Type of error")
    http_status_code: Optional[int] = Field(
        default=None,
        description="HTTP status code if applicable",
    )
    content: Optional[str] = Field(
        default=None,
        description="Error details",
    )


class ExtractResponse(BaseModel):
    """Response from Extract API."""

    model_config = ConfigDict(extra="allow")

    extract_id: str = Field(..., description="Unique extraction ID")
    results: list[ExtractResult] = Field(
        default_factory=list,
        description="Successful extraction results",
    )
    errors: list[ExtractError] = Field(
        default_factory=list,
        description="Failed extraction errors",
    )
    warnings: Optional[list[dict]] = Field(
        default=None,
        description="Non-fatal warnings",
    )
    usage: Optional[dict] = Field(
        default=None,
        description="API usage statistics",
    )
