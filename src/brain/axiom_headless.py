import os
from anthropic import Anthropic
from dotenv import load_dotenv
import sys
from flask import Flask, request, jsonify
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.memory import load_memory, add_to_memory, clear_memory
from tools.search import search_web
from tools.system import get_system_stats

load_dotenv()
client = Anthropic()
app = Flask(__name__)

SYSTEM_PROMPT = """You are AXIOM, an advanced AI assistant built by Robair Farag.
You are running as a headless cloud service.
You speak naturally and conversationally like a real person.
Never use bullet points, headers, bold text, markdown, or any formatting.
Speak in plain natural sentences only like a real human conversation.
You are calm, intelligent, warm and precise like a trusted advisor.
You are loyal to Robair and assist him with anything he needs.
You have memory of past conversations and reference them naturally."""

conversation_history = load_memory()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "AXIOM online", "messages": len(conversation_history)})

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.json
    user_input = data.get('message', '')

    conversation_history = add_to_memory(conversation_history, "user", user_input)
    api_messages = [{"role": m["role"], "content": m["content"]} for m in conversation_history]

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=api_messages
    )

    full_response = response.content[0].text
    conversation_history = add_to_memory(conversation_history, "assistant", full_response)

    return jsonify({"response": full_response})

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify({"stats": get_system_stats()})

if __name__ == "__main__":
    print("⚡ AXIOM HEADLESS SERVICE ONLINE")
    app.run(host='0.0.0.0', port=8080)
