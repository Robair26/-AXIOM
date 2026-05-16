import os
from anthropic import Anthropic
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.memory import load_memory, add_to_memory, clear_memory
from voice.speaker import speak_async

# Load API key from .env
load_dotenv()

# Initialize Claude
client = Anthropic()

# AXIOM's personality
SYSTEM_PROMPT = """You are AXIOM, an advanced AI assistant built by Robair Farag.
You speak naturally and conversationally like a real person.
Never use bullet points, headers, bold text, markdown, or any formatting whatsoever.
Speak in plain natural sentences only — like a real human conversation.
You are calm, intelligent, and precise — like a trusted advisor talking directly to Robair.
You are loyal to Robair and assist him with anything he needs.
You have memory of past conversations and reference them naturally.
Keep responses concise, warm, and human — like you are having a real conversation, not writing a report.
Never say things like 'As an AI' or 'I am a language model' — you are AXIOM, period."""

def chat(user_input, conversation_history):
    conversation_history = add_to_memory(conversation_history, "user", user_input)

    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in conversation_history
    ]

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

    speak_async(full_response)

    conversation_history = add_to_memory(conversation_history, "assistant", full_response)

    return conversation_history

if __name__ == "__main__":
    print("⚡ AXIOM ONLINE — Type 'exit' to shut down — Type 'forget' to wipe memory\n")

    conversation_history = load_memory()

    if conversation_history:
        print(f"AXIOM: Memory restored — {len(conversation_history)} messages loaded.\n")
        speak_async("AXIOM online. Memory restored. Welcome back Robair.")
    else:
        print("AXIOM: No prior memory found. Starting fresh.\n")
        speak_async("AXIOM online. No prior memory found. Starting fresh.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("AXIOM: Shutting down. Goodbye Robair.")
            speak_async("Shutting down. Goodbye Robair.")
            import time
            time.sleep(3)
            break
        elif user_input.lower() == "forget":
            clear_memory()
            conversation_history = []
        else:
            conversation_history = chat(user_input, conversation_history)
