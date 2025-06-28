from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict, Optional

#  Define proper schema for LangGraph
class AgentState(TypedDict, total=False):
    user_input: str
    booking_time: Optional[str]
    response: Optional[str]

# Handle the chat logic
def handle_input(state: AgentState) -> AgentState:
    user_input = state.get("user_input", "").lower()

    if "book" in user_input or "meeting" in user_input:
        if any(word in user_input for word in ["tomorrow", "am", "pm", "at", "in", "/", "-", ":"]):
            state["booking_time"] = user_input
            return {"response": "Got it! Booking the meeting...", **state}
        else:
            return {"response": "When would you like to schedule the meeting?", **state}
    else:
        return {"response": "Hi! You can ask me to book a meeting like 'tomorrow at 5 PM'.", **state}

# Build the LangGraph agent
def build_agent():
    graph = StateGraph(AgentState)
    graph.add_node("input", RunnableLambda(handle_input))
    graph.set_entry_point("input")
    graph.set_finish_point("input")
    return graph.compile()
