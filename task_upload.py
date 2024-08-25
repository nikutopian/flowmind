import os
from pathlib import Path
from typing import TypedDict, List, Annotated, Dict
import operator
from flow_mind_state import FlowMindContext

def task_upload(context: FlowMindContext) -> FlowMindContext:
    # Simulating file upload
    uploaded_file = input("Enter the path of the file to upload: ")
    
    if not uploaded_file:
        return FlowMindContext(
            uploaded_file="",
            all_actions=context["all_actions"] + ["Error: No file uploaded"]
        )
    
    # Check if the file exists
    if not os.path.exists(uploaded_file):
        return FlowMindContext(
            uploaded_file="",
            all_actions=context["all_actions"] + [f"Error: File {uploaded_file} not found"]
        )
    
    # Get file extension
    file_extension = Path(uploaded_file).suffix.lower()
    
    # Check if the file type is supported
    supported_extensions = ['.pdf', '.docx', '.png', '.jpg', '.jpeg']
    if file_extension not in supported_extensions:
        return FlowMindContext(
            uploaded_file="",
            all_actions=context["all_actions"] + [f"Error: Unsupported file type: {file_extension}"]
        )
    
    # If everything is okay, return the file path and add an action
    return FlowMindContext(
        uploaded_file=uploaded_file,
        all_actions=context["all_actions"] + [f"File uploaded successfully: {uploaded_file}"]
    )