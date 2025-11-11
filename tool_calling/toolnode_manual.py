from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode
from langgraph.runtime import Runtime


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

tool_node = ToolNode(tools = tools)

message_with_tool_call = AIMessage(
    content='',
    tool_calls=[{'name': 'get_restaurant_recommendations', 'args': {'location': 'munich'}, 'id': '3e896282-6500-4877-bbed-779067c8b61f', 'type': 'tool_call'}]
)
#
#
result = tool_node.invoke({
        "messages": [message_with_tool_call],
    }, runtime=Runtime()
)


print(result)