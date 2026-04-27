from langgraph.graph import StateGraph, END, START
from core.state import AgentState
from core.nodes import strategist_node, executor_node, evaluator_node

workflow = StateGraph(AgentState)

workflow.add_node("strategist", strategist_node)
workflow.add_node("executor", executor_node)
workflow.add_node("evaluator", evaluator_node)

workflow.add_edge(START, "strategist")
workflow.add_edge("strategist", "executor")
workflow.add_edge("executor", "evaluator")

def route_evaluator(state: AgentState) -> str:
    if state.get('status') == 'bug_found':
        return END
    if state.get('loop_count', 0) >= 3:
        return END
    return "strategist"

workflow.add_conditional_edges("evaluator", route_evaluator)

app = workflow.compile()
