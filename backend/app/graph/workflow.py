from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from ..schemas.state import AgentState
from ..agents.summarizer import summarizer_agent
from ..agents.counter import counter_agent

def _get_input_text(state: AgentState) -> str:
    input_text = state.get("input_text")
    if isinstance(input_text, str) and input_text.strip():
        return input_text

    messages = state.get("messages") if isinstance(state, dict) else None
    if isinstance(messages, list):
        for message in reversed(messages):
            if isinstance(message, dict):
                role = message.get("role") or message.get("type")
                if role in {"user", "human"}:
                    content = message.get("content")
                    if isinstance(content, str) and content.strip():
                        return content
            else:
                role = getattr(message, "role", None) or getattr(message, "type", None)
                if role in {"user", "human"}:
                    content = getattr(message, "content", None)
                    if isinstance(content, str) and content.strip():
                        return content
    return ""

def _model_dump(value):
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "dict"):
        return value.dict()
    return value

async def summarize_node(state: AgentState):
    input_text = _get_input_text(state)
    if not input_text:
        return {"summary_data": {"summary": "", "key_points": []}}
    print("Input text to summarize:", input_text)
    try:
        res = await summarizer_agent.run(input_text)
        if hasattr(res, "data"):
            summary = res.data
        elif hasattr(res, "output"):
            summary = res.output
        else:
            summary = res
    except Exception as exc:  # pylint: disable=broad-except
        # Fallback to a naive summary to keep the graph running
        print("Summarizer failed, falling back to naive summary:", exc)
        summary = {"summary": input_text[:300], "key_points": []}
    if isinstance(summary, str):
        summary_payload = {"summary": summary.strip(), "key_points": []}
    elif isinstance(summary, dict) and "summary" in summary:
        summary_payload = summary
    else:
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
    input_text = _get_input_text(state)
    text_to_count = summary_text or input_text or ""
    word_count = len([w for w in text_to_count.split() if w.strip()])
    count_payload = {"word_count": word_count}
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
