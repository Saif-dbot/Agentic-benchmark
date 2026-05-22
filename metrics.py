from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from typing import Any

import psutil


@dataclass
class MetricResult:
    completion: float
    latency_seconds: float
    error_rate: float
    tool_calls_count: int


@dataclass
class ResourceMetrics:
    cpu_percent: float
    ram_mb: float
    gpu_util_percent: float | None
    gpu_memory_mb: float | None


def _read_gpu_metrics() -> tuple[float | None, float | None]:
    command = [
        "nvidia-smi",
        "--query-gpu=utilization.gpu,memory.used",
        "--format=csv,noheader,nounits",
    ]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None, None

    output = completed.stdout.strip().splitlines()
    if not output:
        return None, None

    first_line = output[0].strip()
    if not first_line:
        return None, None

    parts = [part.strip() for part in first_line.split(",")]
    if len(parts) < 2:
        return None, None

    try:
        return float(parts[0]), float(parts[1])
    except ValueError:
        return None, None


def collect_resource_metrics(start_cpu_time: float, elapsed_seconds: float) -> ResourceMetrics:
    process = psutil.Process(os.getpid())
    current_cpu_time = sum(process.cpu_times()[:2])
    cpu_time_delta = max(current_cpu_time - start_cpu_time, 0.0)
    cpu_count = psutil.cpu_count(logical=True) or 1
    cpu_percent = 0.0
    if elapsed_seconds > 0:
        cpu_percent = (cpu_time_delta / elapsed_seconds) * 100.0 / cpu_count

    ram_mb = process.memory_info().rss / (1024 * 1024)
    gpu_util_percent, gpu_memory_mb = _read_gpu_metrics()

    return ResourceMetrics(
        cpu_percent=round(cpu_percent, 3),
        ram_mb=round(ram_mb, 3),
        gpu_util_percent=round(gpu_util_percent, 3) if gpu_util_percent is not None else None,
        gpu_memory_mb=round(gpu_memory_mb, 3) if gpu_memory_mb is not None else None,
    )


def compute_metrics(run_items: list[dict[str, Any]]) -> MetricResult:
    total = len(run_items)
    if total == 0:
        return MetricResult(0.0, 0.0, 0.0, 0)

    completed = len([item for item in run_items if not item.get("error") and item.get("response")])
    avg_latency = sum(float(item.get("latency_seconds", 0.0)) for item in run_items) / total
    errors = len([item for item in run_items if item.get("error")])
    tool_calls = sum(len(item.get("tool_calls", [])) for item in run_items)

    return MetricResult(
        completion=completed / total,
        latency_seconds=avg_latency,
        error_rate=errors / total,
        tool_calls_count=tool_calls,
    )
