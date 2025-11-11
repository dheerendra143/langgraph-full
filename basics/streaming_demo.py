from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from util.langgraph_util import display

class HelloWorldSate(TypedDict):
    message: str


def hello(state: HelloWorldSate):
    print(f"Hello Node: {state['message']}")
    return {"message": "hello " + state["message"]}

def bye(state: HelloWorldSate):
    print(f"Bye Node: {state['message']}")
    return {"message": "Bye " + state["message"]}

graph = StateGraph(HelloWorldSate)
graph.add_node("hello", hello)
graph.add_node("bye", bye)

graph.add_edge(START, "hello")
# graph.set_entry_point("hello")

graph.add_edge("hello", "bye")
graph.add_edge("bye", END)

runnable = graph.compile()
# display(runnable)

for chunk in runnable.stream({"message": "Bharath"},stream_mode="updates"):
    print(chunk)
