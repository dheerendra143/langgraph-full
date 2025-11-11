from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from util.langgraph_util import display


@tool
def get_restaurant_recommendations(location: str):
    """Provide a list"""
    recommendations = {
        "munich": ["hof", "auhets", "Tantris"],
        "newyork": ["Le bernardin", "ambroise", "bistrot paul"],
        "paris": ["le meurice", "eleven madision park", "joes pizza"]
    }

    return recommendations.get(location.lower(), ["No Recommendations available for this location"])


tools = [get_restaurant_recommendations]

# Add tool with model
model = ChatOllama(model="llama3.2").bind_tools(tools)

tool_node = ToolNode(tools = tools)

def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": response}


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
            return "agent"
    return END


workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)


workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")


checkpointer = MemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

display(graph)

config = {"configurable": {"thread_id": "1"}}

result = graph.invoke({
        "messages": [HumanMessage(content="Can you recommend just one top restaurant in Paris?" "The response should contain just the restaurant name")],
    },config
)

print(result)