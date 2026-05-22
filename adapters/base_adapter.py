from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import perf_counter
from typing import Any


@dataclass
class AdapterContext:
    framework: str


class AgentAdapter(ABC):
    """Common interface for all benchmark adapters."""

    def __init__(self, framework_name: str) -> None:
        self.framework_name = framework_name

    @abstractmethod
    def run(self, task: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        """Execute one task and return a standardized payload."""

    def _start_timer(self) -> float:
        return perf_counter()

    def _build_result(
        self,
        *,
        task: dict[str, Any],
        prompt: str,
        response: str,
        started_at: float,
        tool_calls: list[dict[str, Any]] | None = None,
        error: str | None = None,
        metadata: dict[str, Any] | None = None,
        token_metrics: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "framework": self.framework_name,
            "task_id": task.get("id"),
            "task_type": task.get("type"),
            "prompt": prompt,
            "response": response,
            "tool_calls": tool_calls or [],
            "latency_seconds": round(perf_counter() - started_at, 6),
            "error": error,
            "metadata": metadata or {},
            "token_metrics": token_metrics or {},
        }
