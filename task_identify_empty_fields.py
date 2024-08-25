from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from typing import TypedDict, List, Annotated, Dict
import operator
from flow_mind_state import FlowMindContext

def task_identify_empty_fields(context: FlowMindContext) -> FlowMindContext:
    parsed_text = context["parsed_text"]
    if not parsed_text:
        return FlowMindContext(
            empty_fields=[],
            all_actions=context["all_actions"] + ["Error: No parsed text provided"]
        )
    
    llm = OpenAI(temperature=0)
    
    prompt = PromptTemplate(
        input_variables=["form_content"],
        template="Identify all empty fields in the following form content:\n\n{form_content}\n\nList of empty fields:"
    )
    
    response = llm(prompt.format(form_content=parsed_text))
    
    # Process the response to extract empty fields
    empty_fields = [field.strip() for field in response.split('\n') if field.strip()]
    
    return FlowMindContext(
        empty_fields=empty_fields,
        all_actions=context["all_actions"] + [f"Identified {len(empty_fields)} empty fields"]
    )