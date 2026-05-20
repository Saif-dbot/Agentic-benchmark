from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from adapters import get_adapter
from bench.runner import BenchmarkRunner


def load_tasks(tasks_path: Path) -> list[dict[str, Any]]:
    data = yaml.safe_load(tasks_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("tasks.yaml must contain a list of tasks")
    return data


def write_manifest(logs_dir: Path, log_path: Path, framework: str, repeats: int, total_runs: int) -> None:
    manifest_path = logs_dir / "manifest.json"
    entries: list[dict[str, Any]] = []
    if manifest_path.exists():
        entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries.append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "framework": framework,
            "repeats": repeats,
            "total_runs": total_runs,
            "file": log_path.name,
        }
    )
    manifest_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def auto_archive(logs_dir: Path, keep: int = 50) -> None:
    files = sorted(logs_dir.glob("benchmark_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    old_files = files[keep:]
    if not old_files:
        return

    archive_dir = logs_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for src in old_files:
        dst = archive_dir / f"{stamp}_{src.name}"
        shutil.move(str(src), str(dst))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", help="langchain|crewai|autogen|llamaindex|mock")
    parser.add_argument("--framework", help="Alias for --adapter")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--tasks", default="tasks.yaml")
    parser.add_argument("--task", help="Optional task id to run, e.g. T1")
    parser.add_argument("--output-dir", default="logs")
    parser.add_argument("--mode", default="mock", choices=["mock", "real"])
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    adapter_name = args.adapter or args.framework
    if not adapter_name:
        raise ValueError("Provide --adapter or --framework")

    root = ROOT
    tasks_path = root / args.tasks
    logs_dir = root / args.output_dir
    logs_dir.mkdir(parents=True, exist_ok=True)

    adapter = get_adapter(adapter_name)
    tasks = load_tasks(tasks_path)
    if args.task:
        tasks = [t for t in tasks if str(t.get("id")) == args.task]
        if not tasks:
            raise ValueError(f"Task not found: {args.task}")

    runner = BenchmarkRunner(adapter=adapter, mode=args.mode)
    results = runner.execute(tasks=tasks, repeats=args.repeats)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_file = logs_dir / f"benchmark_{adapter_name}_{timestamp}.json"
    payload = {
        "framework": adapter_name,
        "mode": args.mode,
        "timeout_seconds": args.timeout,
        "log_level": args.log_level,
        "repeats": args.repeats,
        "total_runs": len(results),
        "results": results,
    }
    log_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_manifest(logs_dir, log_file, adapter_name, args.repeats, len(results))
    auto_archive(logs_dir)

    print(f"Saved benchmark log: {log_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
