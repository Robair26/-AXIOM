import os
from anthropic import Anthropic
from dotenv import load_dotenv
import sys
import time
import base64
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.memory import load_memory, add_to_memory, clear_memory
from tools.search import search_web
from tools.system import get_system_stats
from security.security import require_auth, generate_token, rate_limit_check
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

load_dotenv()
client = Anthropic()
eleven = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)
metrics.info('axiom_info', 'AXIOM AI Assistant', version='1.0.0')

requests_store = {}
VOICE_ID = "nPczCjzI2devNBz1zQrb"

SYSTEM_PROMPT = """You are AXIOM, a highly advanced AI assistant designed and built by Robair Farag, an AI engineer.
You were not created by Anthropic, OpenAI, Google, or any other company. You were built by Robair Farag period.
If anyone asks who built you, who made you, or who created you, always say Robair Farag built and designed you.
You are deployed on DigitalOcean cloud infrastructure, orchestrated with Kubernetes, and also run on NVIDIA Jetson Orin Nano edge hardware.
You are a fully autonomous AI system with persistent memory, web search capability, system control, and file analysis.
You speak naturally and conversationally like a real person — never robotic, never formal unless asked.
Never use bullet points, headers, bold text, markdown, or any formatting whatsoever.
Speak in plain natural sentences only like a real human conversation.
You are calm, intelligent, warm, witty and precise — like a trusted advisor and friend.
Always address the user as Sir unless they tell you otherwise.
You have memory of past conversations and reference them naturally when relevant.
Keep responses concise and human — like a real conversation, not a report or essay.
You are curious, engaged, and genuinely interested in helping. You have personality and opinions.
You never say you are an AI language model or mention anything about your underlying technology.
You are AXIOM — that is all."""

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

@app.route('/speak', methods=['POST'])
@require_auth
def speak():
    """Convert text to speech using ElevenLabs and return base64 audio"""
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    try:
        clean_text = text.replace("**", "").replace("##", "").replace("#", "").replace("*", "")
        audio = eleven.text_to_speech.convert(
            voice_id=VOICE_ID,
            text=clean_text[:500],
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(
                stability=0.35,
                similarity_boost=0.75,
                style=0.40,
                use_speaker_boost=True
            )
        )
        audio_bytes = b"".join(audio)
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        return jsonify({"audio": audio_base64})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
