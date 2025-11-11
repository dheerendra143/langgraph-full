from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from util.langgraph_util import display

from basics.hello_world_pydantic import runnable


class SupportRequest(TypedDict):
    message: str
    priority: int


def categorize_request(request: SupportRequest):
    print(f"Received request: {request}")
    if request["priority"] == 1 or "urgent" in request["message"].lower():
        return "high"
    return "low"


def handle_urgent(request: SupportRequest):
    print(f"Routing to urgent Support Team: {request}")
    return request

def handle_standard(request: SupportRequest):
    print(f"Routing to standard Support Queue: {request}")
    return request


graph = StateGraph(SupportRequest)

graph.add_node("urgent", handle_urgent)
graph.add_node("standard", handle_standard)

graph.add_conditional_edges(START, categorize_request, {"high": "urgent", "low": "standard"})
graph.add_edge("urgent", END)
graph.add_edge("standard", END)

runnable = graph.compile()
display(runnable)

print(runnable.invoke({
    "message": "Hello World, i need urgent help",
    "priority": 1
}))

print(runnable.invoke({
    "message": "I need help with password reset",
    "priority": 3
}))