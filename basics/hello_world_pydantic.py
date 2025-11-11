from pydantic import BaseModel, Field
from langgraph.graph import END, START, StateGraph
from util.langgraph_util import display

class HelloWorldSate(BaseModel):
    message: str = Field(min_length=1, max_length=19)
    id: int = Field(default=0)


def hello(state: HelloWorldSate):
    print(f"Hello Node: {state.message}")
    return {"message": "hello " + state.message}

def bye(state: HelloWorldSate):
    print(f"Bye Node: {state.message}")
    return {"message": "Bye " + state.message}

graph = StateGraph(HelloWorldSate)
graph.add_node("hello", hello)
graph.add_node("bye", bye)

graph.add_edge(START, "hello")
# graph.set_entry_point("hello")

graph.add_edge("hello", "bye")
graph.add_edge("bye", END)

runnable = graph.compile()
display(runnable)
output = runnable.invoke({"message": "Dheerendra"})
print(output)


