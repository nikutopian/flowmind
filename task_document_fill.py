import json
from typing import Dict, List

from pydantic import BaseModel, Field

from flow_mind_state import FlowMindContext
from llms.llm_factory import LLMFactory


def task_document_fill(context: FlowMindContext) -> FlowMindContext:

    # Get document context and empty fields
    document_context = context.get("parsed_text", "")
    empty_fields = context["empty_fields"]
    context_memory = context.get("context_memory", {})

    # Initialize LLM
    llm = LLMFactory.create_llm("openai", "gpt-4o-mini")

    class DocumentFillResponse(BaseModel):
        filled_fields: Dict[str, str] = Field(
            ..., description="Fields that were successfully filled"
        )
        remaining_fields: List[str] = Field(
            ..., description="Fields that still need to be filled"
        )

    # Update prompt to request specific output format
    # Update prompt to request specific output format
    prompt = f"""Given the following document context:
    {document_context}

    And the following context memory:
    {json.dumps(context_memory, indent=2)}

    Please fill in the following empty fields:
    {json.dumps(empty_fields, indent=2)}

    Use the provided context to fill in as many fields as possible. If a field cannot be filled based on the given context, leave it in the remaining_fields list.

    Provide the output in the following format:
    1. A dictionary of filled_fields where the key is the field name and the value is the filled content.
    2. A list of remaining_fields that couldn't be filled based on the given context.

    Make sure output is in JSON format.
    Ensure your response can be parsed into a DocumentFillResponse object."""
    # Get LLM response
    response: DocumentFillResponse = llm.chat(
        system_prompt="You are a helpful assistant that fills in document fields based on given context.",
        user_prompt=prompt,
        force_json_format=True,
        response_model=DocumentFillResponse,
    )

    context["filled_fields"] = response.filled_fields
    context["empty_fields"] = response.remaining_fields
    context["all_actions"] = context["all_actions"] + [f"Filled {len(response.filled_fields)} fields using context memory"]

    return context
