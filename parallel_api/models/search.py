# ---
# entity_id: module-parallel-search
# entity_name: Search API Models
# entity_type_id: module
# entity_path: parallel_api/models/search.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T18:00:00Z
# entity_exports: [SearchRequest, SearchResponse, SearchResult, SearchMode]
# entity_dependencies: [pydantic]
# entity_callers: [parallel_api, clients]
# entity_callees: []
# entity_semver_impact: major
# entity_breaking_change_risk: medium
# entity_public_api: true
# ---

"""
Pydantic models for Parallel.ai Search API (Beta).

POST /v1beta/search
Web search with natural language objectives or keyword queries.
"""

from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SearchMode(str, Enum):
    """Search processing mode."""

    ONE_SHOT = "one-shot"
    AGENTIC = "agentic"


class ExcerptConfig(BaseModel):
    """Configuration for search result excerpts."""

    model_config = ConfigDict(extra="forbid")

    max_chars_per_result: Optional[int] = Field(
        default=None,
        description="Maximum characters per result excerpt",
    )
    max_chars_total: Optional[int] = Field(
        default=None,
        description="Maximum total characters across all excerpts",
    )


class SourcePolicy(BaseModel):
    """Policy for filtering search sources."""

    model_config = ConfigDict(extra="forbid")

    include_domains: Optional[list[str]] = Field(
        default=None,
        description="Only include results from these domains",
    )
    exclude_domains: Optional[list[str]] = Field(
        default=None,
        description="Exclude results from these domains",
    )
    after_date: Optional[date] = Field(
        default=None,
        description="Only include results published after this date",
    )


class FetchPolicy(BaseModel):
    """Policy for content fetching."""

    model_config = ConfigDict(extra="forbid")

    max_age_seconds: Optional[int] = Field(
        default=None,
        description="Maximum age of cached content",
    )
    timeout_seconds: Optional[int] = Field(
        default=None,
        description="Request timeout",
    )
    disable_cache_fallback: Optional[bool] = Field(
        default=None,
        description="Disable cache fallback",
    )


class SearchRequest(BaseModel):
    """Request body for Search API."""

    model_config = ConfigDict(extra="forbid")

    objective: Optional[str] = Field(
        default=None,
        description="Natural-language description of what the web search is trying to find",
    )
    search_queries: Optional[list[str]] = Field(
        default=None,
        description="Optional list of traditional keyword search queries",
    )
    mode: Optional[SearchMode] = Field(
        default=SearchMode.ONE_SHOT,
        description="Search processing mode",
    )
    max_results: Optional[int] = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results to return",
    )
    excerpts: Optional[ExcerptConfig] = Field(
        default=None,
        description="Excerpt configuration",
    )
    source_policy: Optional[SourcePolicy] = Field(
        default=None,
        description="Source filtering policy",
    )
    fetch_policy: Optional[FetchPolicy] = Field(
        default=None,
        description="Content fetching policy",
    )


class SearchResult(BaseModel):
    """A single search result."""

    model_config = ConfigDict(extra="allow")

    url: str = Field(..., description="Result URL")
    title: Optional[str] = Field(default=None, description="Page title")
    publish_date: Optional[str] = Field(
        default=None,
        description="Publication date",
    )
    excerpts: Optional[list[str]] = Field(
        default=None,
        description="Relevant excerpts from the page",
    )


class SearchResponse(BaseModel):
    """Response from Search API."""

    model_config = ConfigDict(extra="allow")

    search_id: str = Field(..., description="Unique search ID")
    results: list[SearchResult] = Field(
        default_factory=list,
        description="Search results",
    )
    warnings: Optional[list[dict]] = Field(
        default=None,
        description="Non-fatal warnings",
    )
    usage: Optional[list[dict]] = Field(
        default=None,
        description="API usage statistics",
    )
