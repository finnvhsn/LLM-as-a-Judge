import os
from dotenv import load_dotenv

load_dotenv()

from typing import Annotated
from typing_extensions import TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_tavily import TavilySearch

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


# 🧠 Zustand definieren
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 🔧 Tool definieren
tavily_tool = TavilySearch(max_results=5)
tools = [tavily_tool]

# 🤖 LLM + Toolbindung
llm = ChatAnthropic(model="claude-3-haiku-20240307")
llm_with_tools = llm.bind_tools(tools)


# 💬 Chatbot-Node
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# 🛠 Tool-Node (aus LangGraph prebuilt)
tool_node = ToolNode(tools=tools)

# 📌 Graph aufbauen
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge(START, "chatbot")  # optional bei START/END
graph_builder.set_entry_point("chatbot")

# 💾 Memory aktivieren (speichert State für thread_id)
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
