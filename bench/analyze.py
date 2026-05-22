from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _save_barplot(data: pd.DataFrame, x: str, y: str, title: str, output_path: Path) -> None:
    plt.figure(figsize=(10, 5))
    sns.barplot(data=data, x=x, y=y)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def _build_flat_rows(payload: dict[str, object], runs: list[object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for run in runs:
        if isinstance(run, dict):
            resource_metrics = run.get("resource_metrics", {}) if isinstance(run.get("resource_metrics", {}), dict) else {}
            token_metrics = run.get("token_metrics", {}) if isinstance(run.get("token_metrics", {}), dict) else {}
            rows.append(
                {
                    "framework": payload.get("framework"),
                    "task_id": run.get("task_id"),
                    "task_type": run.get("task_type", "unknown"),
                    "latency_seconds": run.get("latency_seconds", 0.0),
                    "has_error": bool(run.get("error")),
                    "has_response": bool(run.get("response")),
                    "cpu_percent": float(resource_metrics.get("cpu_percent", 0.0)),
                    "ram_mb": float(resource_metrics.get("ram_mb", 0.0)),
                    "gpu_util_percent": resource_metrics.get("gpu_util_percent"),
                    "gpu_memory_mb": resource_metrics.get("gpu_memory_mb"),
                    "prompt_tokens": float(token_metrics.get("prompt_tokens", 0.0)),
                    "completion_tokens": float(token_metrics.get("completion_tokens", 0.0)),
                    "total_tokens": float(token_metrics.get("total_tokens", 0.0)),
                }
            )
    return rows


def _build_completion_column(df: pd.DataFrame) -> pd.Series:
    return (~df["has_error"]) & (df["has_response"])


def _write_summaries_and_plots(df: pd.DataFrame, results_dir: Path) -> None:
    df["completion"] = _build_completion_column(df)

    by_framework = (
        df.groupby("framework", as_index=False)
        .agg(
            completion_rate=("completion", "mean"),
            avg_latency_seconds=("latency_seconds", "mean"),
            error_count=("has_error", "sum"),
            avg_cpu_percent=("cpu_percent", "mean"),
            avg_ram_mb=("ram_mb", "mean"),
            avg_prompt_tokens=("prompt_tokens", "mean"),
            avg_completion_tokens=("completion_tokens", "mean"),
            avg_total_tokens=("total_tokens", "mean"),
            total_runs=("task_id", "count"),
        )
        .sort_values("framework")
    )
    by_framework.to_csv(results_dir / "summary_by_framework.csv", index=False)

    by_category = (
        df.groupby(["framework", "task_type"], as_index=False)
        .agg(
            completion_rate=("completion", "mean"),
            avg_latency_seconds=("latency_seconds", "mean"),
            error_count=("has_error", "sum"),
            avg_cpu_percent=("cpu_percent", "mean"),
            avg_ram_mb=("ram_mb", "mean"),
            avg_prompt_tokens=("prompt_tokens", "mean"),
            avg_completion_tokens=("completion_tokens", "mean"),
            avg_total_tokens=("total_tokens", "mean"),
            total_runs=("task_id", "count"),
        )
        .sort_values(["framework", "task_type"])
    )
    by_category.to_csv(results_dir / "summary_by_category.csv", index=False)

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x="framework", y="latency_seconds")
    plt.title("Latency Distribution by Framework")
    plt.tight_layout()
    plt.savefig(results_dir / "latency_boxplot.png", dpi=160)
    plt.close()

    _save_barplot(by_framework, "framework", "completion_rate", "Completion Rate by Framework", results_dir / "completion_rates.png")
    _save_barplot(by_framework, "framework", "avg_total_tokens", "Average Tokens by Framework", results_dir / "token_usage.png")
    _save_barplot(by_framework, "framework", "avg_cpu_percent", "Average CPU Usage by Framework", results_dir / "cpu_usage.png")
    _save_barplot(by_framework, "framework", "avg_ram_mb", "Average RAM Usage by Framework", results_dir / "ram_usage.png")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs-dir", default="logs")
    parser.add_argument("--output-dir", default="results")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    logs_dir = root / args.logs_dir
    results_dir = root / args.output_dir
    results_dir.mkdir(parents=True, exist_ok=True)

    summaries: list[dict[str, object]] = []
    flat_rows: list[dict[str, object]] = []
    for file in sorted(logs_dir.glob("benchmark_*.json")):
        payload = json.loads(file.read_text(encoding="utf-8"))
        runs = payload.get("results", [])
        latencies = [r.get("latency_seconds", 0.0) for r in runs if isinstance(r, dict)]
        avg_latency = (sum(latencies) / len(latencies)) if latencies else 0.0
        error_count = len([r for r in runs if isinstance(r, dict) and r.get("error")])
        cpu_values = [
            float(r.get("resource_metrics", {}).get("cpu_percent", 0.0))
            for r in runs
            if isinstance(r, dict)
        ]
        ram_values = [
            float(r.get("resource_metrics", {}).get("ram_mb", 0.0))
            for r in runs
            if isinstance(r, dict)
        ]
        gpu_util_values = [
            r.get("resource_metrics", {}).get("gpu_util_percent")
            for r in runs
            if isinstance(r, dict) and r.get("resource_metrics", {}).get("gpu_util_percent") is not None
        ]
        gpu_mem_values = [
            r.get("resource_metrics", {}).get("gpu_memory_mb")
            for r in runs
            if isinstance(r, dict) and r.get("resource_metrics", {}).get("gpu_memory_mb") is not None
        ]
        prompt_token_values = [
            float(r.get("token_metrics", {}).get("prompt_tokens", 0.0))
            for r in runs
            if isinstance(r, dict)
        ]
        completion_token_values = [
            float(r.get("token_metrics", {}).get("completion_tokens", 0.0))
            for r in runs
            if isinstance(r, dict)
        ]
        total_token_values = [
            float(r.get("token_metrics", {}).get("total_tokens", 0.0))
            for r in runs
            if isinstance(r, dict)
        ]
        summaries.append(
            {
                "framework": payload.get("framework"),
                "mode": payload.get("mode"),
                "repeats": payload.get("repeats"),
                "total_runs": payload.get("total_runs", len(runs)),
                "avg_latency_seconds": round(avg_latency, 6),
                "error_count": error_count,
                "avg_cpu_percent": round((sum(cpu_values) / len(cpu_values)) if cpu_values else 0.0, 6),
                "avg_ram_mb": round((sum(ram_values) / len(ram_values)) if ram_values else 0.0, 6),
                "avg_gpu_util_percent": round((sum(gpu_util_values) / len(gpu_util_values)) if gpu_util_values else 0.0, 6),
                "avg_gpu_memory_mb": round((sum(gpu_mem_values) / len(gpu_mem_values)) if gpu_mem_values else 0.0, 6),
                "avg_prompt_tokens": round((sum(prompt_token_values) / len(prompt_token_values)) if prompt_token_values else 0.0, 6),
                "avg_completion_tokens": round((sum(completion_token_values) / len(completion_token_values)) if completion_token_values else 0.0, 6),
                "avg_total_tokens": round((sum(total_token_values) / len(total_token_values)) if total_token_values else 0.0, 6),
                "source_file": file.name,
            }
        )

        flat_rows.extend(_build_flat_rows(payload, runs))

    out = results_dir / "analysis.json"
    out.write_text(json.dumps(summaries, indent=2, ensure_ascii=False), encoding="utf-8")

    if flat_rows:
        df = pd.DataFrame(flat_rows)
        _write_summaries_and_plots(df, results_dir)

    print(f"Saved analysis: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
