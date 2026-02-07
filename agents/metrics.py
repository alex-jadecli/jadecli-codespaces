# ---
# entity_id: module-agents-metrics
# entity_name: Agent Metrics System
# entity_type_id: module
# entity_path: agents/metrics.py
# entity_language: python
# entity_state: active
# entity_created: 2026-01-23T00:00:00Z
# entity_exports: [MetricsCollector, AgentMetrics, show_metrics]
# entity_dependencies: [pydantic]
# entity_callers: [orchestrator]
# entity_callees: []
# entity_semver_impact: minor
# entity_breaking_change_risk: low
# ---

"""
Metrics Collection and Reporting for Multi-Agent Orchestration.

Tracks:
- Task execution counts and durations
- Token usage by agent type
- Cost estimates
- Latency percentiles
- Error rates
- Routing decisions

Provides:
- Real-time metrics dashboard
- Historical metrics storage
- Export to various formats
"""

import json
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


@dataclass
class MetricSample:
    """A single metric sample."""

    timestamp: datetime
    value: float
    labels: dict[str, str] = field(default_factory=dict)


class Counter:
    """Monotonically increasing counter metric."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self._value: float = 0
        self._labels: dict[tuple[str, ...], float] = defaultdict(float)

    def inc(self, value: float = 1, **labels: str) -> None:
        """Increment counter."""
        self._value += value
        if labels:
            key = tuple(sorted(labels.items()))
            self._labels[key] += value

    @property
    def value(self) -> float:
        return self._value

    def get(self, **labels: str) -> float:
        """Get counter value for specific labels."""
        key = tuple(sorted(labels.items()))
        return self._labels.get(key, 0)


class Gauge:
    """Gauge metric that can increase or decrease."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self._value: float = 0

    def set(self, value: float) -> None:
        """Set gauge value."""
        self._value = value

    def inc(self, value: float = 1) -> None:
        """Increment gauge."""
        self._value += value

    def dec(self, value: float = 1) -> None:
        """Decrement gauge."""
        self._value -= value

    @property
    def value(self) -> float:
        return self._value


class Histogram:
    """Histogram metric for tracking distributions."""

    def __init__(
        self,
        name: str,
        description: str = "",
        buckets: Optional[list[float]] = None,
    ):
        self.name = name
        self.description = description
        self.buckets = buckets or [10, 50, 100, 250, 500, 1000, 2500, 5000, 10000]
        self._values: list[float] = []
        self._bucket_counts: dict[float, int] = {b: 0 for b in self.buckets}

    def observe(self, value: float) -> None:
        """Record an observation."""
        self._values.append(value)
        for bucket in self.buckets:
            if value <= bucket:
                self._bucket_counts[bucket] += 1

    @property
    def count(self) -> int:
        return len(self._values)

    @property
    def sum(self) -> float:
        return sum(self._values) if self._values else 0

    @property
    def mean(self) -> float:
        return statistics.mean(self._values) if self._values else 0

    def percentile(self, p: float) -> float:
        """Get percentile value."""
        if not self._values:
            return 0
        sorted_values = sorted(self._values)
        idx = int(len(sorted_values) * p / 100)
        return sorted_values[min(idx, len(sorted_values) - 1)]


class AgentMetrics(BaseModel):
    """Summary of agent metrics."""

    # Task counts
    total_tasks: int = 0
    claude_tasks: int = 0
    ollama_tasks: int = 0
    failed_tasks: int = 0
    fallback_count: int = 0

    # Token usage
    total_tokens: int = 0
    claude_tokens: int = 0
    ollama_tokens: int = 0
    tokens_saved: int = 0

    # Cost
    total_cost_usd: float = 0.0
    estimated_savings_usd: float = 0.0

    # Latency (ms)
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0

    # Routing
    ollama_route_percentage: float = 0.0
    avg_routing_confidence: float = 0.0

    # Time range
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class MetricsCollector:
    """
    Collects and aggregates metrics from agent execution.

    Provides:
    - Counter, gauge, and histogram metrics
    - Time-windowed aggregation
    - Export capabilities
    """

    def __init__(self):
        """Initialize metrics collector."""
        # Counters
        self.tasks_total = Counter("tasks_total", "Total tasks executed")
        self.tasks_by_agent = Counter("tasks_by_agent", "Tasks by agent type")
        self.tokens_total = Counter("tokens_total", "Total tokens used")
        self.tokens_by_agent = Counter("tokens_by_agent", "Tokens by agent type")
        self.errors_total = Counter("errors_total", "Total errors")
        self.fallbacks_total = Counter("fallbacks_total", "Total fallbacks")

        # Gauges
        self.active_tasks = Gauge("active_tasks", "Currently active tasks")
        self.cost_total = Gauge("cost_total_usd", "Total cost in USD")

        # Histograms
        self.latency = Histogram(
            "latency_ms",
            "Task latency in milliseconds",
            buckets=[10, 50, 100, 250, 500, 1000, 2500, 5000],
        )
        self.routing_confidence = Histogram(
            "routing_confidence",
            "Routing decision confidence",
            buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        )

        # Time tracking
        self._start_time = datetime.utcnow()
        self._samples: list[MetricSample] = []

    def record_task_start(self, task_id: UUID, agent_type: str) -> None:
        """Record task start."""
        self.active_tasks.inc()
        self._samples.append(MetricSample(
            timestamp=datetime.utcnow(),
            value=1,
            labels={"event": "task_start", "task_id": str(task_id), "agent": agent_type},
        ))

    def record_task_complete(
        self,
        task_id: UUID,
        agent_type: str,
        duration_ms: float,
        tokens: int,
        cost_usd: float,
        success: bool = True,
    ) -> None:
        """Record task completion."""
        self.active_tasks.dec()
        self.tasks_total.inc()
        self.tasks_by_agent.inc(agent_type=agent_type)

        self.tokens_total.inc(tokens)
        self.tokens_by_agent.inc(tokens, agent_type=agent_type)

        self.cost_total.inc(cost_usd)
        self.latency.observe(duration_ms)

        if not success:
            self.errors_total.inc(agent_type=agent_type)

        self._samples.append(MetricSample(
            timestamp=datetime.utcnow(),
            value=duration_ms,
            labels={
                "event": "task_complete",
                "task_id": str(task_id),
                "agent": agent_type,
                "success": str(success),
            },
        ))

    def record_routing_decision(
        self,
        agent_type: str,
        confidence: float,
        tokens_saved: int = 0,
    ) -> None:
        """Record routing decision."""
        self.routing_confidence.observe(confidence)

        if tokens_saved > 0:
            self._samples.append(MetricSample(
                timestamp=datetime.utcnow(),
                value=tokens_saved,
                labels={"event": "tokens_saved", "agent": agent_type},
            ))

    def record_fallback(self, from_agent: str, to_agent: str) -> None:
        """Record fallback event."""
        self.fallbacks_total.inc(from_agent=from_agent, to_agent=to_agent)

    def get_summary(self) -> AgentMetrics:
        """Get summary metrics."""
        claude_tasks = self.tasks_by_agent.get(agent_type="claude")
        ollama_tasks = self.tasks_by_agent.get(agent_type="ollama")
        total_tasks = self.tasks_total.value

        # Calculate tokens saved
        claude_tokens = self.tokens_by_agent.get(agent_type="claude")
        ollama_tokens = self.tokens_by_agent.get(agent_type="ollama")
        # Estimate: if Ollama tasks went to Claude, they'd use ~same tokens
        tokens_saved = ollama_tokens

        # Estimate savings (Claude input: $3/M, output: $15/M, avg ~$5/M)
        estimated_savings = tokens_saved * 0.000005

        return AgentMetrics(
            total_tasks=int(total_tasks),
            claude_tasks=int(claude_tasks),
            ollama_tasks=int(ollama_tasks),
            failed_tasks=int(self.errors_total.value),
            fallback_count=int(self.fallbacks_total.value),
            total_tokens=int(self.tokens_total.value),
            claude_tokens=int(claude_tokens),
            ollama_tokens=int(ollama_tokens),
            tokens_saved=int(tokens_saved),
            total_cost_usd=self.cost_total.value,
            estimated_savings_usd=estimated_savings,
            avg_latency_ms=self.latency.mean,
            p50_latency_ms=self.latency.percentile(50),
            p95_latency_ms=self.latency.percentile(95),
            p99_latency_ms=self.latency.percentile(99),
            ollama_route_percentage=(
                ollama_tasks / total_tasks * 100 if total_tasks > 0 else 0
            ),
            avg_routing_confidence=self.routing_confidence.mean,
            start_time=self._start_time,
            end_time=datetime.utcnow(),
        )

    def to_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []

        # Tasks
        lines.append(f"# HELP tasks_total Total tasks executed")
        lines.append(f"# TYPE tasks_total counter")
        lines.append(f"tasks_total {self.tasks_total.value}")

        # Tokens
        lines.append(f"# HELP tokens_total Total tokens used")
        lines.append(f"# TYPE tokens_total counter")
        lines.append(f"tokens_total {self.tokens_total.value}")

        # Cost
        lines.append(f"# HELP cost_total_usd Total cost in USD")
        lines.append(f"# TYPE cost_total_usd gauge")
        lines.append(f"cost_total_usd {self.cost_total.value}")

        # Latency histogram
        lines.append(f"# HELP latency_ms Task latency in milliseconds")
        lines.append(f"# TYPE latency_ms histogram")
        for bucket, count in sorted(self.latency._bucket_counts.items()):
            lines.append(f'latency_ms_bucket{{le="{bucket}"}} {count}')
        lines.append(f"latency_ms_sum {self.latency.sum}")
        lines.append(f"latency_ms_count {self.latency.count}")

        return "\n".join(lines)

    def to_json(self) -> str:
        """Export metrics as JSON."""
        return self.get_summary().model_dump_json(indent=2)


def show_metrics() -> None:
    """Display metrics dashboard in terminal."""
    # This would be called from CLI
    # For now, create a sample display
    print("\n" + "=" * 60)
    print("  MULTI-AGENT METRICS DASHBOARD")
    print("=" * 60)

    print("\nNo active metrics collector. Start the orchestrator first.")
    print("\nUsage:")
    print("  from agents.metrics import MetricsCollector")
    print("  collector = MetricsCollector()")
    print("  # ... use with orchestrator ...")
    print("  print(collector.get_summary())")


def main() -> None:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Agent metrics")
    parser.add_argument("command", choices=["show", "export"])
    parser.add_argument("--format", choices=["json", "prometheus"], default="json")

    args = parser.parse_args()

    if args.command == "show":
        show_metrics()
    elif args.command == "export":
        # Would export from a running collector
        print(f"Export format: {args.format}")
        print("No active collector to export from.")


if __name__ == "__main__":
    main()
