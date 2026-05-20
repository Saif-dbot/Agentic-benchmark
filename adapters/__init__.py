from .autogen_adapter import AutoGenAdapter
from .base_adapter import AgentAdapter
from .crewai_adapter import CrewAIAdapter
from .config import load_config
from .langchain_adapter import LangChainAdapter
from .llamaindex_adapter import LlamaIndexAdapter
from .mock_adapter import MockAdapter


def get_adapter(name: str) -> AgentAdapter:
    key = name.strip().lower()
    mapping = {
        "langchain": LangChainAdapter,
        "crewai": CrewAIAdapter,
        "autogen": AutoGenAdapter,
        "llamaindex": LlamaIndexAdapter,
        "llama-index": LlamaIndexAdapter,
        "mock": MockAdapter,
    }
    if key not in mapping:
        raise ValueError(f"Unsupported adapter: {name}")
    return mapping[key]()
