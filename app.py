from main import graph
from langchain_core.messages import AIMessage

def stream_graph_updates(user_input: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}

    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    ):
        last_msg = event ["messages"][-1]
        
        if isinstance (last_msg, AIMessage):
            content = last_msg.content
            
            if isinstance(content, list) and all(isinstance(c, dict) and c.get("type") == "tool_use" for c in content):
                continue
            print("Assistant:", content)

if __name__ == "__main__":
    thread_id = input("🧠 Konversations-ID (z. B. '1'): ").strip() or "1"
    print(f"💬 Starte Konversation mit thread_id = {thread_id}\n")

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input, thread_id)
        except Exception as e:
            print("Fehler:", e)
            break
