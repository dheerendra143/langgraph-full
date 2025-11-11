from operator import add
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph, MessagesState


class ChatBontState(MessagesState):
    discount: Annotated[int, add]

def connect_to_sales(state: MessagesState):
    return {"messages": [AIMessage(content="Great! let me connect you with our sales team right away")]}

def sales_response(state: MessagesState):
    return {"messages": [AIMessage(content="We have best offer for your")]}



graph_builder = StateGraph(MessagesState)

graph_builder.add_node("connect_to_sales", connect_to_sales)
graph_builder.add_node("sales_response", sales_response)



graph_builder.add_edge(START,"connect_to_sales")
graph_builder.add_edge("connect_to_sales", "sales_response")
graph_builder.add_edge("sales_response", END)


chatbot = graph_builder.compile()

test_input = "I want to buy your product"


messages = chatbot.invoke({"messages": [HumanMessage(content=test_input)]})

for message in messages["messages"]:
    print(f"****Bot** {message.content}")
