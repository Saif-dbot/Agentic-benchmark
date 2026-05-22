"""Generate a LaTeX longtable appendix from tasks.yaml.

The output is written to report/tasks_appendix.tex.
"""
from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TASKS_YAML = ROOT / "tasks.yaml"
OUT_TEX = ROOT / "report" / "tasks_appendix.tex"


def parse_tasks(text: str):
    tasks = []
    current = {}
    for line in text.splitlines():
        if line.startswith("- id:"):
            if current:
                tasks.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif current and line.strip().startswith("title:"):
            current["title"] = line.split(":", 1)[1].strip().strip('"')
        elif current and line.strip().startswith("type:"):
            current["type"] = line.split(":", 1)[1].strip()
    if current:
        tasks.append(current)
    return tasks


def latex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "_": r"\_",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def main() -> None:
    text = TASKS_YAML.read_text(encoding="utf-8")
    tasks = parse_tasks(text)
    lines = []
    lines.append(r"\begin{longtable}{@{}lll@{}}")
    lines.append(r"\caption{Liste complète des 120 tâches du benchmark.}\label{tab:alltasks}\\")
    lines.append(r"\toprule")
    lines.append(r"ID & Titre & Type \\")
    lines.append(r"\midrule")
    lines.append(r"\endfirsthead")
    lines.append(r"\toprule")
    lines.append(r"ID & Titre & Type \\")
    lines.append(r"\midrule")
    lines.append(r"\endhead")
    for task in tasks:
        lines.append(
            "{} & {} & {} \\\\".format(
                latex_escape(task.get('id', '')),
                latex_escape(task.get('title', '')),
                latex_escape(task.get('type', '')),
            )
        )
    lines.append(r"\bottomrule")
    lines.append(r"\end{longtable}")
    OUT_TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_TEX} with {len(tasks)} tasks")


if __name__ == "__main__":
    main()
