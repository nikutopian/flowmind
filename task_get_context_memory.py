import json

def task_get_context_memory(state):
    empty_fields = state.get("empty_fields")
    if not empty_fields:
        return {"error": "No empty fields provided"}
    
    # Simulating retrieval from a JSON file
    try:
        with open('user_context.json', 'r') as f:
            user_context = json.load(f)
    except FileNotFoundError:
        return {"error": "User context file not found"}
    
    filled_fields = {}
    for field in empty_fields:
        if field in user_context:
            filled_fields[field] = user_context[field]
    
    return {"filled_fields": filled_fields}
