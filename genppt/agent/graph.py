from langgraph.graph import END, StateGraph

from genppt.agent.nodes import build_pptx, fetch_assets, plan_slides
from genppt.agent.state import AgentState


def create_graph():
    """
    Build and compile the LangGraph StateGraph.

    Flow:
        plan_slides → fetch_assets → build_pptx → END

    fetch_assets internally uses asyncio.gather so image fetching and icon
    resolution run concurrently within that node.  Adding new tool nodes
    (e.g. web_search, chart_generator) is as simple as inserting them into
    this graph and wiring edges.
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("plan_slides", plan_slides)
    workflow.add_node("fetch_assets", fetch_assets)
    workflow.add_node("build_pptx", build_pptx)

    workflow.set_entry_point("plan_slides")
    workflow.add_edge("plan_slides", "fetch_assets")
    workflow.add_edge("fetch_assets", "build_pptx")
    workflow.add_edge("build_pptx", END)

    return workflow.compile()


# Module-level compiled graph — import and invoke directly.
graph = create_graph()
