from typing import TypedDict, List, Annotated, Dict
import operator
from flow_mind_state import FlowMindContext
import json
import os
from pathlib import Path

def task_get_context_memory(context: FlowMindContext) -> FlowMindContext:
    # Placeholder implementation
    # In a real scenario, you would retrieve context from a database or file

    # Read from personal history file
    personal_context_path = Path("./context/personal_context.json")
    if personal_context_path.exists():
        with open(personal_context_path, "r") as f:
            context_memory = json.load(f)
    else:
        print(f"Warning: Personal context file not found at {personal_context_path}")
        context_memory = {}

    # Ask user for additional documents
    while True:
        additional_doc = input("Enter path to additional document (or press Enter to skip): ").strip()
        if not additional_doc:
            break
        
        doc_path = Path(additional_doc)
        if doc_path.exists() and doc_path.is_file():
            with open(doc_path, "r") as f:
                additional_context = json.load(f)
            context_memory.update(additional_context)
            print(f"Added context from {doc_path}")
        else:
            print(f"Warning: File not found or is not a file: {doc_path}")

    # If context_memory is still empty after attempts to populate it, use a default
    if not context_memory:
        print("Warning: No context memory retrieved")
        context_memory = {"default": "No context memory retrieved"}

    return FlowMindContext(
        context_memory=context_memory,
        all_actions=context["all_actions"] + ["Retrieved context memory"]
    )