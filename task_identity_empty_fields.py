from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

def task_identify_empty_fields(state):
    parsed_text = state.get("parsed_text")
    if not parsed_text:
        return {"error": "No parsed text provided"}
    
    llm = OpenAI(temperature=0)
    
    prompt = PromptTemplate(
        input_variables=["form_content"],
        template="Identify all empty fields in the following form content:\n\n{form_content}\n\nList of empty fields:"
    )
    
    response = llm(prompt.format(form_content=parsed_text))
    
    # Process the response to extract empty fields
    empty_fields = [field.strip() for field in response.split('\n') if field.strip()]
    
    return {"empty_fields": empty_fields}
