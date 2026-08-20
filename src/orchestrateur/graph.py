from langgraph.graph import StateGraph
from .orchestrateur import run_orchestrateur

workflow = StateGraph()

workflow.add_node("orchestrateur", run_orchestrateur)

workflow.set_entry_point("orchestrateur")

app = workflow.compile()
