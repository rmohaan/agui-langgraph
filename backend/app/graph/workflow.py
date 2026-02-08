from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from ..schemas.state import AgentState
from ..agents.summarizer import summarizer_agent
from ..agents.counter import counter_agent

def _model_dump(value):
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "dict"):
        return value.dict()
    return value

async def summarize_node(state: AgentState):
    print("Input text to summarize:", state["input_text"])
    res = await summarizer_agent.run(state["input_text"])
    summary = res.data if hasattr(res, "data") else res
    summary_payload = _model_dump(summary)
    state["summary_data"] = summary_payload
    return {"summary_data": summary_payload}

async def count_node(state: AgentState):
    print("Summary to count words in:", state["summary_data"])
    summary_data = state.get("summary_data")
    if isinstance(summary_data, dict):
        summary_text = summary_data.get("summary")
    else:
        summary_text = getattr(summary_data, "summary", None)
    res = await counter_agent.run(summary_text or state["input_text"])
    count = res.data if hasattr(res, "data") else res
    count_payload = _model_dump(count)
    state["final_count"] = count_payload
    return {"final_count": count_payload}

workflow = StateGraph(AgentState)
workflow.add_node("summarizer", summarize_node)
workflow.add_node("counter", count_node)
workflow.add_edge(START, "summarizer")
workflow.add_edge("summarizer", "counter")
workflow.add_edge("counter", END)

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
