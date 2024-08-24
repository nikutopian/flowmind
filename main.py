import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import Graph
from langgraph.prebuilt.tool_executor import ToolExecutor
from task_document_parse import task_document_parse
from task_document_fill import task_document_fill
from task_upload import task_upload
from task_generate_ui import task_generate_ui
from task_get_context_memory import task_get_context_memory
from task_identity_empty_fields import task_identify_empty_fields


# Load environment variables
load_dotenv()

# Initialize OpenAI API
llm = ChatOpenAI(model="gpt-4")

# Create the workflow graph
workflow = Graph()

# Add nodes to the graph
workflow.add_node("upload", task_upload)
workflow.add_node("parse", task_document_parse)
workflow.add_node("identify_fields", task_identify_empty_fields)
workflow.add_node("get_context", task_get_context_memory)
workflow.add_node("fill_document", task_document_fill)
workflow.add_node("generate_ui", task_generate_ui)

# Define edges (connections between nodes)
workflow.add_edge("upload", "parse")
workflow.add_edge("parse", "identify_fields")
workflow.add_edge("identify_fields", "get_context")
workflow.add_edge("get_context", "fill_document")
workflow.add_edge("fill_document", "generate_ui")

# Compile the graph
app = workflow.compile()

# Run the workflow
initial_state = {}  # Define initial state
for output in app.stream(initial_state):
    print(output)