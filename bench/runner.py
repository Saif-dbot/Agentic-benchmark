from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from adapters.base_adapter import AgentAdapter


@dataclass
class BenchmarkRunner:
    adapter: AgentAdapter
    mode: str = "mock"

    def execute(self, tasks: list[dict[str, Any]], repeats: int) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for _ in range(repeats):
            for task in tasks:
                results.append(self.adapter.run(task, config={"mode": self.mode}))
        return results
