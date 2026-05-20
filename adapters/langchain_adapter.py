from __future__ import annotations

import os
from typing import Any

from .base_adapter import AgentAdapter
from .config import load_config


class LangChainAdapter(AgentAdapter):
    def __init__(self) -> None:
        super().__init__("LangChain")

    def run(self, task: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
        started = self._start_timer()
        prompt = str(task.get("prompt", ""))
        mode = str(config.get("mode", "mock")).lower()

        if mode != "real":
            response = (
                "[MOCK-LANGCHAIN] Reponse simulee. "
                f"Task={task.get('id')} | Type={task.get('type')}"
            )
            return self._build_result(
                task=task,
                prompt=prompt,
                response=response,
                started_at=started,
                metadata={"mode": mode},
            )

        try:
            try:
                runtime_cfg = load_config()
            except Exception:
                runtime_cfg = {}

            model_name = str(runtime_cfg.get("model", "gpt-4o-mini"))
            temperature = float(runtime_cfg.get("temperature", 0.2))
            api_key_env = str(runtime_cfg.get("api_key_env", "OPENAI_API_KEY"))
            api_key = os.getenv(api_key_env, "")

            if not api_key:
                raise RuntimeError(
                    f"API key absente: variable d'environnement '{api_key_env}' non definie"
                )

            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(model=model_name, temperature=temperature, api_key=api_key)
            output = llm.invoke(prompt)
            response_text = str(getattr(output, "content", "") or "")

            return self._build_result(
                task=task,
                prompt=prompt,
                response=response_text,
                started_at=started,
                metadata={
                    "mode": mode,
                    "model": model_name,
                    "temperature": temperature,
                    "api_key_env": api_key_env,
                },
            )
        except Exception as exc:
            return self._build_result(
                task=task,
                prompt=prompt,
                response="",
                started_at=started,
                error=str(exc),
                metadata={"mode": mode},
            )
