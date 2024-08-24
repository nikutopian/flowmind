from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

def task_generate_ui(state):
    empty_fields = state.get("empty_fields")
    filled_fields = state.get("filled_fields", {})
    
    remaining_fields = [field for field in empty_fields if field not in filled_fields]
    
    if not remaining_fields:
        return {"message": "All fields are filled. No UI needed."}
    
    llm = OpenAI(temperature=0.7)
    
    prompt = PromptTemplate(
        input_variables=["fields"],
        template="Generate HTML for a form with the following fields:\n\n{fields}\n\nHTML:"
    )
    
    response = llm(prompt.format(fields="\n".join(remaining_fields)))
    
    return {"ui_html": response}
