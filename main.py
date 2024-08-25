from enum import Enum, auto
from typing import Dict, List, Callable, TypedDict, Annotated
import operator
from task_upload import task_upload
from task_document_parse import task_document_parse
from task_identify_empty_fields import task_identify_empty_fields
from task_get_context_memory import task_get_context_memory
from task_document_fill import task_document_fill
from task_generate_ui import task_generate_ui
from flow_mind_state import FlowMindContext, FlowMindState

class StateGraph:
    def __init__(self):
        self.states: Dict[FlowMindState, List[FlowMindState]] = {state: [] for state in FlowMindState}
        self.actions: Dict[FlowMindState, Callable[[FlowMindContext], FlowMindContext]] = {}
        self.context: FlowMindContext = FlowMindContext(
            uploaded_file="",
            parsed_text="",
            empty_fields=[],
            filled_fields={},
            ui_html="",
            all_actions=[]
        )

    def add_transition(self, from_state: FlowMindState, to_state: FlowMindState):
        self.states[from_state].append(to_state)

    def add_action(self, state: FlowMindState, action: Callable[[FlowMindContext], FlowMindContext]):
        self.actions[state] = action

    def get_next_states(self, state: FlowMindState) -> List[FlowMindState]:
        return self.states[state]

    def execute_action(self, state: FlowMindState) -> None:
        if state in self.actions:
            new_context = self.actions[state](self.context)
            self.context.update(new_context)

class WorkflowManager:
    def __init__(self, state_graph: StateGraph):
        self.state_graph = state_graph
        self.current_state = FlowMindState.TaskUpload

    def run(self):
        while self.current_state != FlowMindState.End:
            print(f"Executing state: {self.current_state.name}")
            self.state_graph.execute_action(self.current_state)
            next_states = self.state_graph.get_next_states(self.current_state)
            if next_states:
                self.current_state = next_states[0]  # For simplicity, we're just taking the first next state
            else:
                self.current_state = FlowMindState.End
        print("Workflow completed.")
        print("All actions:", self.state_graph.context["all_actions"])

# Example usage
def main():
    graph = StateGraph()

    # Define transitions
    graph.add_transition(FlowMindState.TaskUpload, FlowMindState.TaskDocumentParse)
    graph.add_transition(FlowMindState.TaskDocumentParse, FlowMindState.TaskIdentifyEmptyFields)
    graph.add_transition(FlowMindState.TaskIdentifyEmptyFields, FlowMindState.TaskGetContext_Memory)
    graph.add_transition(FlowMindState.TaskGetContext_Memory, FlowMindState.TaskDocumentFill)
    graph.add_transition(FlowMindState.TaskDocumentFill, FlowMindState.TaskGenerateUI)
    graph.add_transition(FlowMindState.TaskGenerateUI, FlowMindState.End)

    # Define actions
    graph.add_action(FlowMindState.TaskUpload, task_upload)
    graph.add_action(FlowMindState.TaskDocumentParse, task_document_parse)
    graph.add_action(FlowMindState.TaskIdentifyEmptyFields, task_identify_empty_fields)
    graph.add_action(FlowMindState.TaskGetContext_Memory, task_get_context_memory)
    graph.add_action(FlowMindState.TaskDocumentFill, task_document_fill)
    graph.add_action(FlowMindState.TaskGenerateUI, task_generate_ui)

    # Run the workflow
    workflow = WorkflowManager(graph)
    workflow.run()

if __name__ == "__main__":
    main()