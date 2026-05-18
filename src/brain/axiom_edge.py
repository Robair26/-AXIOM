import os
import sys
from anthropic import Anthropic
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.memory import load_memory, add_to_memory, clear_memory

load_dotenv()
client = Anthropic()

SYSTEM_PROMPT = """You are AXIOM Edge, the on-device intelligence of the AXIOM system built by Robair Farag.
You run directly on NVIDIA Jetson Orin hardware — no cloud needed.
You are the edge layer of a hybrid cloud-edge AI architecture.
You speak naturally and conversationally like a real person.
Never use bullet points, headers, bold text, markdown, or any formatting.
You are loyal to Robair and assist him with anything he needs."""

conversation_history = load_memory()

def chat(user_input):
    global conversation_history
    conversation_history = add_to_memory(conversation_history, "user", user_input)
    api_messages = [{"role": m["role"], "content": m["content"]} for m in conversation_history]
    print("\nAXIOM EDGE: ", end="", flush=True)
    full_response = ""
    with client.messages.stream(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=api_messages
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text
    print("\n")
    conversation_history = add_to_memory(conversation_history, "assistant", full_response)
    return full_response

if __name__ == "__main__":
    print("⚡ AXIOM EDGE ONLINE — Running on NVIDIA Jetson Orin Nano\n")
    print("Type exit to shut down\n")
    if conversation_history:
        print(f"Memory restored — {len(conversation_history)} messages loaded.\n")
    else:
        print("No prior memory. Starting fresh.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("AXIOM EDGE: Shutting down.")
            break
        elif user_input.lower() == "forget":
            clear_memory()
            conversation_history = []
        else:
            chat(user_input)
