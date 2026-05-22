from __future__ import annotations

from adapters import get_adapter

REQUIRED_KEYS = {
    "framework",
    "task_id",
    "task_type",
    "prompt",
    "response",
    "tool_calls",
    "latency_seconds",
    "error",
    "metadata",
    "token_metrics",
}


def validate_result(name: str, result: dict) -> None:
    missing = REQUIRED_KEYS.difference(result.keys())
    if missing:
        raise AssertionError(f"{name}: missing keys {sorted(missing)}")


if __name__ == "__main__":
    task = {"id": "T_TEST", "type": "sanity", "prompt": "Hello"}
    for name in ["langchain", "crewai", "autogen", "llamaindex"]:
        adapter = get_adapter(name)
        output = adapter.run(task=task, config={"mode": "mock"})
        validate_result(name, output)
        print(f"{name}: OK")
    print("All adapters return the expected schema.")
