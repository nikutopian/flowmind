from enum import Enum
from typing import Any, Dict, Type

from llms.llm_base import LLM
from llms.llm_implementations import (
    ClaudeLLM,
    GroqLLM,
    OpenAILLM,
)
from llms.model_types import (
    ClaudeModelType,
    GroqModelType,
    OpenAIModelType,
)


class LLMServiceMap:
    llm_classes: Dict[str, Type[LLM]] = {
        "openai": OpenAILLM,
        "claude": ClaudeLLM,
        "groq": GroqLLM,
    }

    llm_model_names: Dict[str, Enum] = {
        "openai": OpenAIModelType,
        "claude": ClaudeModelType,
        "groq": GroqModelType,
    }


class LLMFactory:

    @classmethod
    def register_llm(cls, service: str, llm_class: Type[LLM]):
        LLMServiceMap.llm_classes[service.lower()] = llm_class

    @classmethod
    def create_llm(cls, service: str, model: str, **kwargs) -> LLM:
        llm_class = LLMServiceMap.llm_classes.get(service.lower())
        if llm_class is None:
            raise ValueError(f"Unsupported LLM service: {service}")
        return llm_class(model, **kwargs)

    @classmethod
    def create_llm_from_config(cls, config: Dict[str, Any]) -> LLM:
        service = config.pop("service")
        model = config.pop("model")
        return cls.create_llm(service, model, **config)
