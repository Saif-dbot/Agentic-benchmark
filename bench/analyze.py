from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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
        error_count = sum(1 for r in runs if isinstance(r, dict) and r.get("error"))
        summaries.append(
            {
                "framework": payload.get("framework"),
                "mode": payload.get("mode"),
                "repeats": payload.get("repeats"),
                "total_runs": payload.get("total_runs", len(runs)),
                "avg_latency_seconds": round(avg_latency, 6),
                "error_count": error_count,
                "source_file": file.name,
            }
        )

        for run in runs:
            if not isinstance(run, dict):
                continue
            flat_rows.append(
                {
                    "framework": payload.get("framework"),
                    "task_id": run.get("task_id"),
                    "task_type": run.get("task_type", "unknown"),
                    "latency_seconds": run.get("latency_seconds", 0.0),
                    "has_error": bool(run.get("error")),
                    "has_response": bool(run.get("response")),
                }
            )

    out = results_dir / "analysis.json"
    out.write_text(json.dumps(summaries, indent=2, ensure_ascii=False), encoding="utf-8")

    if flat_rows:
        df = pd.DataFrame(flat_rows)
        df["completion"] = (~df["has_error"]) & (df["has_response"])

        by_framework = (
            df.groupby("framework", as_index=False)
            .agg(
                completion_rate=("completion", "mean"),
                avg_latency_seconds=("latency_seconds", "mean"),
                error_count=("has_error", "sum"),
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

        plt.figure(figsize=(10, 5))
        sns.barplot(data=by_framework, x="framework", y="completion_rate")
        plt.ylim(0, 1)
        plt.title("Completion Rate by Framework")
        plt.tight_layout()
        plt.savefig(results_dir / "completion_rates.png", dpi=160)
        plt.close()

    print(f"Saved analysis: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
