
from main import graph

def stream_graph_updates(user_input: str):
    result = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
    print("Assistant:", result["messages"][-1].content)

if __name__ == "__main__":
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input)
        except:
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break
