from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = "config.json"


def load_config(config_path: str = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    cfg = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        raise ValueError("config.json must contain a JSON object")

    api_key_env = cfg.get("api_key_env")
    if isinstance(api_key_env, str) and api_key_env:
        cfg["api_key_present"] = bool(os.getenv(api_key_env))
    else:
        cfg["api_key_present"] = False

    return cfg
