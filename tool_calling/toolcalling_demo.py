from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def get_restaurant_recommendations(location: str):
    """Provide a list of restaurant recommendations for a given location"""
    recommendations = {
        "munich": ["hof", "auhets", "Tantris"],
        "new york": ["Le bernardin", "ambroise", "bistrot paul"],
        "paris": ["le meurice", "eleven madision park", "joes pizza"]
    }

    return recommendations.get(location.lower(), ["No Recommendations available for this location"])


tools = [get_restaurant_recommendations]

llm = ChatOpenAI()

# llm = ChatOpenAI(model="gemma:2b")
# llm = ChatOllama(model="gemma:2b")

llm_with_tools = llm.bind_tools(tools)

messages = [
    HumanMessage("Recommend some restaurant in munich")
]


llm_output = llm.invoke("what is the indial capital")

print(llm_output)