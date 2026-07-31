import os
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver #ntemporal memory
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(model="gpt-5.4", temperature=0.7)

# State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#chatbot node
def chatbot(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# Build graph
graph_builder = StateGraph(ChatState)

# Add nodes
graph_builder.add_node("chatbot", chatbot)

# Add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile(checkpointer=InMemorySaver())