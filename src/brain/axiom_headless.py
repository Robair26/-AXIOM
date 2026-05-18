import os
from anthropic import Anthropic
from dotenv import load_dotenv
import sys
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.memory import load_memory, add_to_memory, clear_memory
from tools.search import search_web
from tools.system import get_system_stats
from security.security import require_auth, generate_token, rate_limit_check

load_dotenv()
client = Anthropic()
app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)
metrics.info('axiom_info', 'AXIOM AI Assistant', version='1.0.0')

requests_store = {}

SYSTEM_PROMPT = """You are AXIOM, an advanced AI assistant.
You are running as a headless cloud service.
You speak naturally and conversationally like a real person.
Never use bullet points, headers, bold text, markdown, or any formatting.
Speak in plain natural sentences only like a real human conversation.
You are calm, intelligent, warm and precise like a trusted advisor.
Always address the user as Sir.
You have memory of past conversations and reference them naturally.
Keep responses concise and human like a real conversation not a report."""

conversation_history = load_memory()

@app.route('/')
def ui():
    return send_from_directory('/app/src/ui', 'index.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "AXIOM online", "messages": len(conversation_history)})

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    password = data.get('password', '')
    axiom_password = os.getenv('AXIOM_PASSWORD', 'axiom2024')
    if password == axiom_password:
        token = generate_token()
        return jsonify({"token": token})
    return jsonify({"error": "Invalid password"}), 401

@app.route('/chat', methods=['POST'])
@require_auth
@metrics.counter('axiom_chat_requests', 'Number of chat requests')
def chat():
    global conversation_history
    ip = request.remote_addr
    if not rate_limit_check(ip, requests_store):
        return jsonify({"error": "Rate limit exceeded"}), 429
    start_time = time.time()
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
    response_time = time.time() - start_time
    return jsonify({"response": full_response, "response_time": response_time})

@app.route('/stats', methods=['GET'])
@require_auth
def stats():
    return jsonify({"stats": get_system_stats()})

@app.route('/memory/clear', methods=['DELETE'])
@require_auth
def clear():
    global conversation_history
    clear_memory()
    conversation_history = []
    return jsonify({"status": "Memory cleared"})

if __name__ == "__main__":
    print("⚡ AXIOM HEADLESS SERVICE ONLINE — SECURED + MONITORED")
    app.run(host='0.0.0.0', port=8080)
