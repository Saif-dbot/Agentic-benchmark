from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class MetricResult:
    completion: float
    latency_seconds: float
    error_rate: float
    tool_calls_count: int


def compute_metrics(run_items: list[dict[str, Any]]) -> MetricResult:
    total = len(run_items)
    if total == 0:
        return MetricResult(0.0, 0.0, 0.0, 0)

    completed = sum(1 for item in run_items if not item.get("error") and item.get("response"))
    avg_latency = sum(float(item.get("latency_seconds", 0.0)) for item in run_items) / total
    errors = sum(1 for item in run_items if item.get("error"))
    tool_calls = sum(len(item.get("tool_calls", [])) for item in run_items)

    return MetricResult(
        completion=completed / total,
        latency_seconds=avg_latency,
        error_rate=errors / total,
        tool_calls_count=tool_calls,
    )
