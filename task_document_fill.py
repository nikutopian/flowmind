def task_document_fill(state):
    parsed_text = state.get("parsed_text")
    filled_fields = state.get("filled_fields")
    
    if not parsed_text or not filled_fields:
        return {"error": "Missing parsed text or filled fields"}
    
    # This is a simplified implementation. In a real-world scenario,
    # you'd need to handle different document formats (PDF, DOCX, etc.)
    filled_document = parsed_text
    
    for field, value in filled_fields.items():
        # Replace empty field placeholders with filled values
        filled_document = filled_document.replace(f"[{field}]", value)
    
    return {"filled_document": filled_document}
