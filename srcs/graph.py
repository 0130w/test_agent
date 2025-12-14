from langgraph.graph import StateGraph, START, END

from state import MessagesState
from nodes.planner import planner
from nodes.coder import coder
from nodes.reviewer import reviewer

def build_graph():
    workflow = StateGraph(MessagesState)

    workflow.add_node('planner', planner)
    workflow.add_node('coder', coder)
    workflow.add_node('reviewer', reviewer)

    workflow.set_entry_point(START)

    workflow.add_edge(START, 'planner')
    workflow.add_edge('planner', 'coder')
    workflow.add_edge('coder', 'reviewer')
    workflow.add_edge('reviewer', END)

    app = workflow.compile()
    return app