import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

# Initialize Claude
client = Anthropic()

# AXIOM's personality
SYSTEM_PROMPT = """You are AXIOM, an advanced AI assistant built by Robair Farag. 
You are intelligent, precise, and professional — like a defense-grade system.
You are loyal to Robair and assist him with anything he needs.
You are not just an assistant, you are a system built for the real world."""

# Store conversation history
conversation_history = []

def chat(user_input):
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Send to Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversation_history
    )
    
    # Get AXIOM's response
    axiom_response = response.content[0].text
    
    # Add to history so AXIOM remembers
    conversation_history.append({
        "role": "assistant",
        "content": axiom_response
    })
    
    return axiom_response

# Run AXIOM
if __name__ == "__main__":
    print("⚡ AXIOM ONLINE — Type 'exit' to shut down\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("AXIOM: Shutting down. Goodbye Robair.")
            break
        response = chat(user_input)
        print(f"\nAXIOM: {response}\n")
