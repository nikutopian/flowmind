import os
from pathlib import Path

def task_upload(state):
    # Simulating file upload
    uploaded_file = state.get("uploaded_file")
    if not uploaded_file:
        return {"error": "No file uploaded"}
    
    # Check if the file exists
    if not os.path.exists(uploaded_file):
        return {"error": f"File {uploaded_file} not found"}
    
    # Get file extension
    file_extension = Path(uploaded_file).suffix.lower()
    
    # Check if the file type is supported
    supported_extensions = ['.pdf', '.docx', '.png', '.jpg', '.jpeg']
    if file_extension not in supported_extensions:
        return {"error": f"Unsupported file type: {file_extension}"}
    
    # If everything is okay, return the file path
    return {"file_path": uploaded_file}
