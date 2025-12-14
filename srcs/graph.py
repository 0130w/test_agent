from langgraph.graph import StateGraph, END

from srcs.state import MessagesState
from srcs.nodes.planner import planner
from srcs.nodes.coder import coder
from srcs.nodes.reviewer import reviewer

def build_graph():
    workflow = StateGraph(MessagesState)

    workflow.add_node('planner', planner)
    workflow.add_node('coder', coder)
    workflow.add_node('reviewer', reviewer)

    workflow.set_entry_point('planner')

    workflow.add_edge('planner', 'coder')
    workflow.add_edge('coder', 'reviewer')
    workflow.add_edge('reviewer', END)

    app = workflow.compile()
    return app