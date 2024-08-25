from flow_mind_state import FlowMindState

def task_document_finalize(state: FlowMindState):
    filled_document = state.get("filled_document")
    
    return {"filled_document": filled_document}
