from operator import add
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph


class ChatBontState(TypedDict):
    message: Annotated[list[AnyMessage], add]
    discount: Annotated[int, add]

def connect_to_sales(state: ChatBontState):
    return {"message": [AIMessage(content="Great! let me connect you with our sales team right away")],
            "discount": 10,}

def sales_response(state: ChatBontState):
    return {"message": [AIMessage(content="We have best offer for your")],
            "discount": 20,}



graph_builder = StateGraph(ChatBontState)

graph_builder.add_node("connect_to_sales", connect_to_sales)
graph_builder.add_node("sales_response", sales_response)



graph_builder.add_edge(START,"connect_to_sales")
graph_builder.add_edge("connect_to_sales", "sales_response")
graph_builder.add_edge("sales_response", END)


chatbot = graph_builder.compile()

test_input = "I want to buy your product"


messages = chatbot.invoke({"message": [HumanMessage(content=test_input)]})

for message in messages["message"]:
    print(f"****Bot** {message.content}")

print("Final discount", messages['discount'],' %')