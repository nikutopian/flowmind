from pathlib import Path
from flow_mind_state import FlowMindContext
from file_parser import FileParser


def task_document_parse(context: FlowMindContext) -> FlowMindContext:
    file_path = context["uploaded_file"]
    if not file_path:
        context["all_actions"] = context["all_actions"] + [
            "Error: No file path provided"
        ]
        return context

    file_extension = Path(file_path).suffix.lower()

    if file_extension in [".png", ".jpg", ".jpeg", ".pdf", ".docx"]:
        fp = FileParser()

        parsed_text = fp.parse_file(file_path)
        context["parsed_text"] = parsed_text
        return context
    else:
        context["all_actions"] = context["all_actions"] + [
            f"Error: Unsupported file type: {file_extension}"
        ]
        return context
