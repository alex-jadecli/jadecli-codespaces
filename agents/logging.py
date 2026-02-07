# ---
# entity_id: module-agents-logging
# entity_name: Agent Logging System
# entity_type_id: module
# entity_path: agents/logging.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [AgentLogger, setup_logging, get_logger, LogLevel]
# entity_dependencies: [structlog, rich]
# entity_callers: [orchestrator, router, ollama_client]
# entity_callees: []
# entity_semver_impact: minor
# entity_breaking_change_risk: low
# ---

"""
Structured Logging System for Multi-Agent Orchestration.

Provides:
- Rich console output with colors and formatting
- Structured JSON logging for machine parsing
- Context propagation for tracing task execution
- Token usage and latency tracking
- Integration with observability tools

Log Levels:
- DEBUG: Detailed debugging information
- INFO: Normal operation events
- WARNING: Potential issues
- ERROR: Errors that affect task execution
- CRITICAL: System-level failures
"""

import json
import logging
import sys
from contextlib import contextmanager
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Generator, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class LogLevel(str, Enum):
    """Log levels with rich formatting."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEvent(BaseModel):
    """Structured log event."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    level: LogLevel
    message: str
    logger_name: str = "agent"

    # Context
    task_id: Optional[UUID] = None
    agent_type: Optional[str] = None
    model_name: Optional[str] = None

    # Metrics
    duration_ms: Optional[float] = None
    tokens_used: Optional[int] = None
    cost_usd: Optional[float] = None

    # Additional data
    extra: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "message": self.message,
            "logger": self.logger_name,
        }
        if self.task_id:
            data["task_id"] = str(self.task_id)
        if self.agent_type:
            data["agent_type"] = self.agent_type
        if self.model_name:
            data["model_name"] = self.model_name
        if self.duration_ms is not None:
            data["duration_ms"] = self.duration_ms
        if self.tokens_used is not None:
            data["tokens_used"] = self.tokens_used
        if self.cost_usd is not None:
            data["cost_usd"] = self.cost_usd
        if self.extra:
            data.update(self.extra)
        return data


class RichConsoleHandler(logging.Handler):
    """Handler that outputs rich-formatted logs to console."""

    # ANSI color codes
    COLORS = {
        LogLevel.DEBUG: "\033[36m",     # Cyan
        LogLevel.INFO: "\033[32m",      # Green
        LogLevel.WARNING: "\033[33m",   # Yellow
        LogLevel.ERROR: "\033[31m",     # Red
        LogLevel.CRITICAL: "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Level symbols
    SYMBOLS = {
        LogLevel.DEBUG: "•",
        LogLevel.INFO: "✓",
        LogLevel.WARNING: "⚠",
        LogLevel.ERROR: "✗",
        LogLevel.CRITICAL: "☠",
    }

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record with rich formatting."""
        try:
            level = LogLevel(record.levelname)
            color = self.COLORS.get(level, "")
            symbol = self.SYMBOLS.get(level, "•")

            # Format timestamp
            timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")

            # Build message parts
            parts = [
                f"{self.DIM}{timestamp}{self.RESET}",
                f"{color}{self.BOLD}{symbol}{self.RESET}",
                record.getMessage(),
            ]

            # Add context if available
            if hasattr(record, "task_id") and record.task_id:
                parts.append(f"{self.DIM}[task:{str(record.task_id)[:8]}]{self.RESET}")
            if hasattr(record, "agent_type") and record.agent_type:
                parts.append(f"{self.DIM}[{record.agent_type}]{self.RESET}")
            if hasattr(record, "duration_ms") and record.duration_ms:
                parts.append(f"{self.DIM}({record.duration_ms:.0f}ms){self.RESET}")
            if hasattr(record, "tokens_used") and record.tokens_used:
                parts.append(f"{self.DIM}[{record.tokens_used} tokens]{self.RESET}")

            # Output
            print(" ".join(parts), file=sys.stderr)

        except Exception:
            self.handleError(record)


class JsonFileHandler(logging.Handler):
    """Handler that outputs JSON logs to a file."""

    def __init__(self, filepath: Path):
        """Initialize JSON file handler."""
        super().__init__()
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record as JSON."""
        try:
            event = LogEvent(
                timestamp=datetime.fromtimestamp(record.created),
                level=LogLevel(record.levelname),
                message=record.getMessage(),
                logger_name=record.name,
                task_id=getattr(record, "task_id", None),
                agent_type=getattr(record, "agent_type", None),
                model_name=getattr(record, "model_name", None),
                duration_ms=getattr(record, "duration_ms", None),
                tokens_used=getattr(record, "tokens_used", None),
                cost_usd=getattr(record, "cost_usd", None),
            )

            with open(self.filepath, "a") as f:
                f.write(json.dumps(event.to_dict()) + "\n")

        except Exception:
            self.handleError(record)


class AgentLogger:
    """
    Logger for multi-agent task execution.

    Provides:
    - Structured logging with context
    - Rich console output
    - JSON file logging
    - Metric tracking
    """

    def __init__(
        self,
        name: str = "agent",
        level: LogLevel = LogLevel.INFO,
        log_file: Optional[Path] = None,
    ):
        """Initialize agent logger."""
        self.name = name
        self._logger = logging.getLogger(name)
        self._logger.setLevel(getattr(logging, level.value))

        # Clear existing handlers
        self._logger.handlers.clear()

        # Add rich console handler
        console_handler = RichConsoleHandler()
        console_handler.setLevel(getattr(logging, level.value))
        self._logger.addHandler(console_handler)

        # Add JSON file handler if specified
        if log_file:
            file_handler = JsonFileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)  # Log everything to file
            self._logger.addHandler(file_handler)

        # Context for tracking
        self._context: dict[str, Any] = {}

    def _log(
        self,
        level: LogLevel,
        message: str,
        **kwargs: Any,
    ) -> None:
        """Internal logging method."""
        # Merge context with kwargs
        extra = {**self._context, **kwargs}

        # Create record with extra attributes
        record = self._logger.makeRecord(
            self.name,
            getattr(logging, level.value),
            "",
            0,
            message,
            (),
            None,
        )

        # Add extra attributes
        for key, value in extra.items():
            setattr(record, key, value)

        self._logger.handle(record)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        self._log(LogLevel.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self._log(LogLevel.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self._log(LogLevel.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self._log(LogLevel.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message."""
        self._log(LogLevel.CRITICAL, message, **kwargs)

    @contextmanager
    def task_context(
        self,
        task_id: UUID,
        agent_type: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> Generator[None, None, None]:
        """Context manager for task-scoped logging."""
        old_context = self._context.copy()
        self._context.update({
            "task_id": task_id,
            "agent_type": agent_type,
            "model_name": model_name,
        })
        try:
            yield
        finally:
            self._context = old_context

    def log_task_start(
        self,
        task_id: UUID,
        agent_type: str,
        model_name: str,
        prompt_preview: str = "",
    ) -> None:
        """Log task start event."""
        preview = prompt_preview[:50] + "..." if len(prompt_preview) > 50 else prompt_preview
        self.info(
            f"Task started: {preview}",
            task_id=task_id,
            agent_type=agent_type,
            model_name=model_name,
        )

    def log_task_complete(
        self,
        task_id: UUID,
        agent_type: str,
        model_name: str,
        duration_ms: float,
        tokens_used: int,
        cost_usd: float = 0.0,
    ) -> None:
        """Log task completion event."""
        self.info(
            f"Task completed",
            task_id=task_id,
            agent_type=agent_type,
            model_name=model_name,
            duration_ms=duration_ms,
            tokens_used=tokens_used,
            cost_usd=cost_usd,
        )

    def log_routing_decision(
        self,
        task_id: UUID,
        agent_type: str,
        model_name: str,
        confidence: float,
        reasoning: str,
    ) -> None:
        """Log routing decision."""
        self.debug(
            f"Routing to {agent_type}: {reasoning} (confidence: {confidence:.2f})",
            task_id=task_id,
            agent_type=agent_type,
            model_name=model_name,
        )

    def log_fallback(
        self,
        task_id: UUID,
        from_agent: str,
        to_agent: str,
        reason: str,
    ) -> None:
        """Log fallback event."""
        self.warning(
            f"Fallback from {from_agent} to {to_agent}: {reason}",
            task_id=task_id,
            agent_type=to_agent,
        )


# Global logger instance
_global_logger: Optional[AgentLogger] = None


def setup_logging(
    level: LogLevel = LogLevel.INFO,
    log_file: Optional[Path] = None,
) -> AgentLogger:
    """Set up global logging configuration."""
    global _global_logger
    _global_logger = AgentLogger(
        name="agent",
        level=level,
        log_file=log_file,
    )
    return _global_logger


def get_logger() -> AgentLogger:
    """Get the global logger instance."""
    global _global_logger
    if _global_logger is None:
        _global_logger = setup_logging()
    return _global_logger
