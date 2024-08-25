from typing import TypedDict, List, Annotated, Dict
import operator
from flow_mind_state import FlowMindContext
from llms.llm_factory import LLMFactory
from llms.model_types import ClaudeModelType

def task_generate_ui(context: FlowMindContext) -> FlowMindContext:
    # Initialize LLM
    llm = LLMFactory.create_llm("claude", ClaudeModelType.CLAUDE35_SONNET.value)

    # Prepare context for LLM
    document_context = context.get("parsed_text", {})
    empty_fields = context["empty_fields"]
    filled_fields = context["filled_fields"]

    prompt = f"""Given the following document context:
    {document_context}

    And the following empty fields that need to be filled:
    {empty_fields}

    Generate a React-based interactive UI artifact to collect the remaining information from the user. The UI should:
    1. Be user-friendly and intuitive
    2. Use appropriate input types for each field (e.g., date picker for dates, dropdown for predefined options)
    3. Include any relevant information from the document context to help the user fill in the fields
    4. Use React hooks for state management
    5. Include basic styling using CSS-in-JS (e.g., styled-components or CSS modules)
    6. Handle form submission and validation

    Provide only the React component code (including any necessary imports and styling), without any explanations."""

    # Get LLM response
    react_ui_code = llm.chat(
        system_prompt="You are an expert React developer and UI designer. Create a user-friendly React component based on the given context.",
        user_prompt=prompt,
    )

    # Store the generated React UI code in the context
    context["ui_react_component"] = react_ui_code

    # Add a note about the change to React-based UI
    context["all_actions"] = context["all_actions"] + ["Generated React-based UI for remaining fields"]
    
    return context