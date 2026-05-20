from __future__ import annotations

from typing import Any

from .base_adapter import AgentAdapter


class LlamaIndexAdapter(AgentAdapter):
    def __init__(self) -> None:
        super().__init__("LlamaIndex")

    def run(self, task: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        started = self._start_timer()
        prompt = str(task.get("prompt", ""))
        response = (
            "[MOCK-LLAMAINDEX] Reponse simulee retrieval. "
            f"Task={task.get('id')} | Type={task.get('type')}"
        )
        return self._build_result(
            task=task,
            prompt=prompt,
            response=response,
            started_at=started,
            metadata={"mode": config.get("mode", "mock")},
        )
