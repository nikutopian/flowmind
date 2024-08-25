import os
from enum import Enum
from typing import Any, Tuple

from anthropic import Anthropic
from groq import Groq
import instructor
from instructor.exceptions import IncompleteOutputException
from openai import OpenAI
from pydantic import BaseModel

from llms.llm_base import LLM


class ApiLLM(LLM):
    def __init__(self, model: str, **kwargs):
        super().__init__(model, **kwargs)
        self.json_format_supported = False
        self.pydantic_response_supported = False

    def _get_client(self, force_json_format: bool = False):
        if self.pydantic_response_supported and force_json_format:
            return self.instructor_client
        return self.client

    def chat(
        self,
        system_prompt: str = "",
        user_prompt: str = "",
        force_json_format: bool = False,
        response_model: BaseModel = None,
    ):
        if (
            self.pydantic_response_supported
            and force_json_format
            and response_model is not None
        ):
            try:
                response = self.instructor_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    seed=self.seed,
                    temperature=self.temperature,
                    response_format=(
                        {"type": "json_object"}
                        if force_json_format
                        else {"type": "text"}
                    ),
                    response_model=response_model,
                )
            except IncompleteOutputException as e:
                token_count = e.last_completion.usage.total_tokens
                print(e)
                print(token_count)

            return response

        else:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                seed=self.seed,
                temperature=self.temperature,
                response_format=(
                    {"type": "json_object"} if force_json_format else {"type": "text"}
                ),
            )

        return response.choices[0].message.content

    def chat_stream(
        self,
        system_prompt: str = "",
        user_prompt: str = "",
    ):
        response_stream = self.client.chat.completions.create(
            model=self.model.value,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            seed=self.seed,
            temperature=self.temperature,
            stream=True,
        )
        for response in response_stream:
            yield response.choices[0].delta.content


class OpenAILLM(ApiLLM):
    def __init__(self, model: str):
        super().__init__(model=model)
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.instructor_client = instructor.from_openai(self.client)
        self.pydantic_response_supported = True


class GroqLLM(ApiLLM):
    def __init__(self, model: str):
        super().__init__(model=model)
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.instructor_client = instructor.from_groq(
            self.client, mode=instructor.Mode.TOOLS
        )
        self.pydantic_response_supported = True


class ClaudeLLM(ApiLLM):
    def __init__(self, model: str):
        super().__init__(model=model)
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.instructor_client = instructor.from_anthropic(self.client)
        self.pydantic_response_supported = True

    def chat(
        self,
        system_prompt: str = "",
        user_prompt: str = "",
        force_json_format: bool = False,
        response_model: BaseModel = None,
    ):
        client = self.client
        kwargs = {}
        expect_pydantic = False
        if (
            self.pydantic_response_supported
            and force_json_format
            and response_model is not None
        ):
            kwargs["response_model"] = response_model
            expect_pydantic = True
            client = self.instructor_client

        response = client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.temperature,
            max_tokens=4096,
            **kwargs,
        )

        if expect_pydantic:
            return response

        return response.content[0].text

    def chat_stream(
        self,
        system_prompt: str = "",
        user_prompt: str = "",
    ):
        response_stream = self.client.messages.create(
            model=self.model.value,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.temperature,
            max_tokens=4096,
            stream=True,
        )
        for response in response_stream:
            if response.type == "content_block_delta":
                yield response.delta.text

