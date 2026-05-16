import os
from anthropic import Anthropic
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.memory import load_memory, add_to_memory, clear_memory

# Load API key from .env
load_dotenv()

# Initialize Claude
client = Anthropic()

# AXIOM's personality
SYSTEM_PROMPT = """You are AXIOM, an advanced AI assistant built by Robair Farag. 
You are intelligent, precise, and professional — like a defense-grade system.
You are loyal to Robair and assist him with anything he needs.
You are not just an assistant, you are a system built for the real world.
You have memory of past conversations with Robair and can reference them."""

def chat(user_input, conversation_history):
    # Add user message to memory
    conversation_history = add_to_memory(conversation_history, "user", user_input)

    # Strip timestamps for API call
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in conversation_history
    ]

    # Stream response from Claude
    print("\nAXIOM: ", end="", flush=True)
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

    # Save AXIOM's response to memory
    conversation_history = add_to_memory(conversation_history, "assistant", full_response)

    return conversation_history

# Run AXIOM
if __name__ == "__main__":
    print("⚡ AXIOM ONLINE — Type 'exit' to shut down — Type 'forget' to wipe memory\n")
    
    # Load existing memory
    conversation_history = load_memory()
    
    if conversation_history:
        print(f"AXIOM: Memory restored — {len(conversation_history)} messages loaded.\n")
    else:
        print("AXIOM: No prior memory found. Starting fresh.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("AXIOM: Shutting down. Goodbye Robair.")
            break
        elif user_input.lower() == "forget":
            clear_memory()
            conversation_history = []
        else:
            conversation_history = chat(user_input, conversation_history)
