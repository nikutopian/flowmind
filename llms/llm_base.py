from abc import ABC, abstractmethod
from typing import Generator
from pydantic import BaseModel


class LLM(ABC):
    def __init__(self, model: str, **kwargs):
        self.model = model
        self.seed = kwargs.get("seed", 42)
        self.temperature = kwargs.get("temperature", 0.1)
        self.api_key = kwargs.get("api_key")

    @abstractmethod
    def chat(
        self,
        system_prompt: str = "",
        user_prompt: str = "",
        force_json_format: bool = False,
        response_model: BaseModel = None,
    ) -> str:
        pass

    @abstractmethod
    def chat_stream(
        self,
        system_prompt: str = "",
        user_prompt: str = "",
    ) -> Generator[str, None, None]:
        pass
