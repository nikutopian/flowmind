from typing import Annotated, List, Dict
from typing_extensions import TypedDict
import operator
from enum import Enum, auto

# Define the state
class FlowMindState(Enum):
    TaskUpload = auto()
    TaskDocumentParse = auto()
    TaskIdentifyEmptyFields = auto()
    TaskGetContext_Memory = auto()
    TaskDocumentFill = auto()
    TaskGenerateUI = auto()
    End = auto()

class FlowMindContext(TypedDict):
    uploaded_file: str
    parsed_text: str
    empty_fields: List[str]
    filled_fields: Dict[str, str]
    ui_react_component: str
    all_actions: Annotated[List[str], operator.add]
