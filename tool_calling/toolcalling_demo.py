from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

@tool
def get_restaurant_recommendations(location: str):
    """Provide a list"""
    recommendations = {
        "munich": ["hof", "auhets", "Tantris"],
        "new york": ["Le bernardin", "ambroise", "bistrot paul"],
        "paris": ["le meurice", "eleven madision park", "joes pizza"]
    }

    return recommendations.get(location.lower(), ["No Recommendations available for this location"])


tools = [get_restaurant_recommendations]

llm = ChatOllama(model="llama3.2")

llm_with_tools = llm.bind_tools(tools)

messages = [
    HumanMessage("Recommend some restaurant in munich")
]


llm_output = llm_with_tools.invoke(messages)

print(llm_output)