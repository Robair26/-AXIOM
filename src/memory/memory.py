import json
import os
from datetime import datetime

# Memory file location
MEMORY_FILE = "config/axiom_memory.json"

def load_memory():
    """Load conversation history from file"""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(conversation_history):
    """Save conversation history to file"""
    with open(MEMORY_FILE, "w") as f:
        json.dump(conversation_history, f, indent=2)

def add_to_memory(conversation_history, role, content):
    """Add a message to memory"""
    conversation_history.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    save_memory(conversation_history)
    return conversation_history

def clear_memory():
    """Wipe AXIOM's memory"""
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    print("AXIOM: Memory wiped.")
