from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any
import sys

from adapters.base_adapter import AgentAdapter
from metrics import collect_resource_metrics


@dataclass
class BenchmarkRunner:
    adapter: AgentAdapter
    mode: str = "mock"

    def execute(
        self,
        tasks: list[dict[str, Any]],
        repeats: int,
        *,
        progress: bool = True,
        progress_label: str | None = None,
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        total_runs = len(tasks) * repeats
        completed_runs = 0
        label = progress_label or self.adapter.framework_name
        for _ in range(repeats):
            for task in tasks:
                start_cpu = 0.0
                process = None
                try:
                    import os
                    import psutil

                    process = psutil.Process(os.getpid())
                    start_cpu = sum(process.cpu_times()[:2])
                except Exception:
                    start_cpu = 0.0

                started_at = perf_counter()
                result = self.adapter.run(task, config={"mode": self.mode})
                elapsed = perf_counter() - started_at

                if process is not None:
                    resources = collect_resource_metrics(start_cpu, elapsed)
                    result = {
                        **result,
                        "resource_metrics": {
                            "cpu_percent": resources.cpu_percent,
                            "ram_mb": resources.ram_mb,
                            "gpu_util_percent": resources.gpu_util_percent,
                            "gpu_memory_mb": resources.gpu_memory_mb,
                        },
                    }
                results.append(result)
                completed_runs += 1
                if progress and total_runs:
                    percent = round((completed_runs / total_runs) * 100, 1)
                    print(
                        f"[{label}] progression {completed_runs}/{total_runs} ({percent}%) - "
                        f"{task.get('id')} / {task.get('type')}",
                        file=sys.stdout,
                        flush=True,
                    )
        return results
