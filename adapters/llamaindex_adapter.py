from __future__ import annotations

from typing import Any

from .base_adapter import AgentAdapter
from .config import load_config
from .local_backend import extract_token_metrics, localize_prompt, ollama_generate_from_config


class LlamaIndexAdapter(AgentAdapter):
    def __init__(self) -> None:
        super().__init__("LlamaIndex")

    def run(self, task: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        started = self._start_timer()
        prompt = localize_prompt(str(task.get("prompt", "")))
        mode = str(config.get("mode", "mock")).lower()

        if mode == "real":
            try:
                runtime_cfg = load_config()
                response_text, raw = ollama_generate_from_config(prompt, runtime_cfg)
                model_name = str(runtime_cfg.get("model", "phi3:mini"))
                temperature = float(runtime_cfg.get("temperature", 0.0))
                base_url = str(runtime_cfg.get("base_url", "http://localhost:11434"))
                token_metrics = extract_token_metrics(raw)
                return self._build_result(
                    task=task,
                    prompt=prompt,
                    response=response_text,
                    started_at=started,
                    metadata={
                        "mode": mode,
                        "model": model_name,
                        "temperature": temperature,
                        "backend": "ollama",
                        "base_url": base_url,
                        "raw_keys": sorted(raw.keys()),
                    },
                    token_metrics=token_metrics,
                )
            except Exception as exc:
                return self._build_result(
                    task=task,
                    prompt=prompt,
                    response="",
                    started_at=started,
                    error=str(exc),
                    metadata={"mode": mode, "backend": "ollama"},
                    token_metrics={},
                )

        response = (
            "[MOCK-LLAMAINDEX] Reponse simulee retrieval. "
            f"Task={task.get('id')} | Type={task.get('type')}"
        )
        return self._build_result(
            task=task,
            prompt=prompt,
            response=response,
            started_at=started,
            metadata={"mode": mode},
            token_metrics={},
        )
