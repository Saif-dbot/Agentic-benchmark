from __future__ import annotations

from pathlib import Path

import yaml

REQUIRED_TASK_KEYS = {"id", "title", "type", "prompt", "expected_format"}
REQUIRED_FRAMEWORK_PROMPTS = {"LangChain", "CrewAI", "AutoGen", "LlamaIndex"}


def main() -> int:
    root = Path(__file__).resolve().parent
    tasks_path = root / "tasks.yaml"
    prompts_path = root / "prompts.yaml"

    tasks = yaml.safe_load(tasks_path.read_text(encoding="utf-8"))
    prompts = yaml.safe_load(prompts_path.read_text(encoding="utf-8"))

    if not isinstance(tasks, list):
        raise ValueError("tasks.yaml doit contenir une liste")
    if not isinstance(prompts, dict):
        raise ValueError("prompts.yaml doit contenir un mapping")

    ids: set[str] = set()
    for item in tasks:
        if not isinstance(item, dict):
            raise ValueError("Chaque tache doit etre un objet YAML")
        missing = REQUIRED_TASK_KEYS.difference(item.keys())
        if missing:
            raise ValueError(f"Tache invalide (cles manquantes): {sorted(missing)}")
        tid = str(item["id"])
        if tid in ids:
            raise ValueError(f"ID duplique: {tid}")
        ids.add(tid)

        if tid not in prompts:
            raise ValueError(f"Prompt manquant pour la tache: {tid}")

        per_framework = prompts[tid]
        if not isinstance(per_framework, dict):
            raise ValueError(f"Prompts invalides pour {tid}")
        missing_frameworks = REQUIRED_FRAMEWORK_PROMPTS.difference(per_framework.keys())
        if missing_frameworks:
            raise ValueError(f"Frameworks manquants pour {tid}: {sorted(missing_frameworks)}")

    print(f"Validation OK: {len(tasks)} taches et prompts coherents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
