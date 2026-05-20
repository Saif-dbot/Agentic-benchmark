from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs-dir", default="logs")
    parser.add_argument("--keep", type=int, default=20, help="Number of newest benchmark logs to keep")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    logs_dir = root / args.logs_dir
    archive_dir = logs_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(logs_dir.glob("benchmark_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    to_archive = files[args.keep :]

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    moved = 0
    for src in to_archive:
        dst = archive_dir / f"{stamp}_{src.name}"
        shutil.move(str(src), str(dst))
        moved += 1

    print(f"Archive done: {moved} files moved to {archive_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
