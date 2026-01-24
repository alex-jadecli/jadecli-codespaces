# ---
# entity_id: module-settings
# entity_name: Centralized Settings
# entity_type_id: module
# entity_path: cli/settings.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-22T17:00:00Z
# entity_exports: [Settings, settings, get_settings]
# entity_dependencies: [pydantic_settings]
# entity_callers: [entity_store, entity_cli, hooks]
# entity_callees: []
# entity_semver_impact: major
# entity_breaking_change_risk: high
# ---

"""
Centralized Settings - Single source of truth for all configuration.

This module provides:
- Pydantic-settings based configuration
- Automatic loading from .env file (local development)
- Support for GitHub secrets (CI/CD)
- Type-safe access to all configuration values

IMPORTANT: All secrets and configuration MUST be accessed through this module.
Never hardcode API keys, secrets, or environment-specific values.

Usage:
    from cli.settings import settings

    # Access configuration
    api_key = settings.parallel_apikey
    db_url = settings.database_url
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Configuration precedence (highest to lowest):
    1. Environment variables
    2. .env file
    3. Default values

    For GitHub Actions, set secrets in:
    - Repository Settings > Secrets > Actions
    - Organization Settings > Secrets (for org-wide)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # === API Keys ===
    parallel_apikey: Optional[str] = Field(
        default=None,
        description="API key for parallel Claude API usage",
    )

    neon_api_key: Optional[str] = Field(
        default=None,
        description="Neon PostgreSQL API key for MCP server",
    )

    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key (if using API directly)",
    )

    github_token: Optional[str] = Field(
        default=None,
        description="GitHub token for API access",
    )

    # === Database ===
    database_url: Optional[str] = Field(
        default=None,
        description="PostgreSQL connection string for Neon",
    )

    # === Environment ===
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Current environment",
    )

    debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )

    # === Entity Store ===
    entity_cache_ttl_hours: int = Field(
        default=24,
        description="Cache TTL for entity index in hours",
    )

    entity_index_path: Path = Field(
        default=Path(".entity-cache"),
        description="Path to entity cache directory",
    )

    # === Parallel Processing ===
    max_parallel_requests: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum parallel API requests",
    )

    request_timeout_seconds: int = Field(
        default=30,
        description="API request timeout in seconds",
    )

    # === Logging ===
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Logging level",
    )

    # === Ollama Configuration ===
    ollama_host: str = Field(
        default="http://localhost:11434",
        description="Ollama server URL",
    )

    ollama_default_model: str = Field(
        default="codellama:7b",
        description="Default Ollama model for code tasks",
    )

    ollama_embedding_model: str = Field(
        default="nomic-embed-text",
        description="Ollama model for embeddings",
    )

    ollama_num_ctx: int = Field(
        default=4096,
        ge=512,
        le=32768,
        description="Ollama context window size",
    )

    ollama_timeout_seconds: int = Field(
        default=60,
        ge=10,
        le=300,
        description="Ollama request timeout",
    )

    # === Multi-Agent Orchestration ===
    agent_prefer_ollama: bool = Field(
        default=True,
        description="Prefer Ollama for supported tasks",
    )

    agent_quality_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum quality threshold for Ollama routing",
    )

    agent_enable_fallback: bool = Field(
        default=True,
        description="Enable fallback from Ollama to Claude",
    )

    agent_track_tokens: bool = Field(
        default=True,
        description="Track token usage for optimization",
    )

    # === Machine Identification ===
    machine_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for this machine",
    )

    agent_id_prefix: str = Field(
        default="wsl",
        description="Prefix for agent IDs",
    )

    @field_validator("entity_index_path", mode="before")
    @classmethod
    def parse_path(cls, v: str | Path) -> Path:
        """Convert string to Path if needed."""
        return Path(v) if isinstance(v, str) else v

    @property
    def is_ci(self) -> bool:
        """Check if running in CI environment."""
        import os
        return bool(os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"))

    @property
    def has_parallel_api(self) -> bool:
        """Check if parallel API key is configured."""
        return bool(self.parallel_apikey)

    @property
    def has_database(self) -> bool:
        """Check if database is configured."""
        return bool(self.database_url or self.neon_api_key)

    @property
    def has_ollama(self) -> bool:
        """Check if Ollama is configured (assumes local availability)."""
        return bool(self.ollama_host)

    @property
    def agent_id(self) -> str:
        """Generate unique agent ID for this machine."""
        import hashlib
        import platform
        machine = self.machine_id or platform.node()
        hash_suffix = hashlib.md5(machine.encode()).hexdigest()[:6]
        return f"{self.agent_id_prefix}-{hash_suffix}"


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Uses lru_cache to ensure settings are only loaded once.
    Call get_settings.cache_clear() to reload.
    """
    return Settings()


# Default settings instance for convenience
settings = get_settings()
