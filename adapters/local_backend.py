from __future__ import annotations

from typing import Any

import requests


MOROCCO_CONTEXT = (
    "Contexte marocain: si une ville, un lieu, une adresse, un montant ou une devise est requis, "
    "utilise des references marocaines comme Rabat, Casablanca, Marrakech, Tanger, Agadir, Fes ou Meknes, "
    "et la devise dirham marocain (MAD)."
)


def localize_prompt(prompt: str) -> str:
    prompt = prompt.strip()
    return MOROCCO_CONTEXT if not prompt else prompt if MOROCCO_CONTEXT in prompt else f"{prompt} {MOROCCO_CONTEXT}"


def extract_token_metrics(raw: dict[str, Any]) -> dict[str, int]:
    prompt_tokens = int(raw.get("prompt_eval_count", 0) or 0)
    completion_tokens = int(raw.get("eval_count", 0) or 0)
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }


def resolve_ollama_settings(runtime_cfg: dict[str, Any]) -> tuple[str, float, int, str]:
    model_name = str(runtime_cfg.get("model", "phi3:mini"))
    temperature = float(runtime_cfg.get("temperature", 0.0))
    max_tokens = int(runtime_cfg.get("max_tokens", 512))
    base_url = str(runtime_cfg.get("base_url", "http://localhost:11434"))
    return model_name, temperature, max_tokens, base_url


def build_ollama_payload(prompt: str, model: str, temperature: float, max_tokens: int) -> dict[str, Any]:
    return {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }


def ollama_generate(
    *,
    prompt: str,
    model: str,
    base_url: str,
    temperature: float,
    max_tokens: int,
) -> tuple[str, dict[str, Any]]:
    url = base_url.rstrip("/") + "/api/generate"
    payload = build_ollama_payload(prompt, model, temperature, max_tokens)
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    return str(data.get("response", "")), data


def ollama_generate_from_config(prompt: str, runtime_cfg: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    model_name, temperature, max_tokens, base_url = resolve_ollama_settings(runtime_cfg)
    return ollama_generate(
        prompt=prompt,
        model=model_name,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
    )