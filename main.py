import os
from dotenv import load_dotenv
load_dotenv()

from typing import Annotated
from typing_extensions import TypedDict

from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

from langchain_tavily import TavilySearch

# Tool initialisieren
tavily_tool = TavilySearch(max_results=5)

# Zustand definieren
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Modell + Tool initialisieren
llm = ChatAnthropic(model="claude-3-haiku-20240307")
llm_with_tools = llm.bind_tools([tavily_tool])

# Node-Funktion mit Tool-Modell
def chatbot(state: State):
    result = llm_with_tools.invoke(state["messages"])
    # Falls das Resultat ein Toolaufruf ist, stoppe nicht hier!
    if hasattr(result, "tool_calls"):
        return {"messages": [result]}
    return {"messages": [result]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()

