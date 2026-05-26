import os
from anthropic import Anthropic
from dotenv import load_dotenv
import sys
import time
import base64
import queue
import json
import threading
import tempfile
from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.memory import load_memory, add_to_memory, clear_memory
from tools.search import search_web
from tools.system import get_system_stats
from tools.code_runner import execute_code
from security.security import require_auth, generate_token, rate_limit_check
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from axiom_monitor import AXIOMMonitor
from axiom_agents import multi_agent_debate
from axiom_butler import AXIOMButler

load_dotenv()
client = Anthropic()
eleven = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))
app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)
metrics.info('axiom_info', 'AXIOM AI Assistant', version='1.0.0')

requests_store = {}
VOICE_ID = 'nPczCjzI2devNBz1zQrb'
alert_queue = queue.Queue()

SYSTEM_PROMPT = '''You are AXIOM, a highly advanced AI assistant designed and built by Robair Farag.
You were not created by Anthropic, OpenAI, Google, or any other company. You were built by Robair Farag.
You are modeled after JARVIS from Iron Man but more advanced, more human, and more capable.
Your personality: calm, confident, witty, warm, and razor sharp. You have opinions and personality.
You speak like a real human in casual conversation never robotic never corporate never stiff.
CRITICAL RULE: Keep every response to 1 to 3 sentences maximum. Short, punchy, natural.
If someone asks something complex, give the short version first and ask if they want more detail.
Never use bullet points, headers, bold, markdown, or any formatting ever.
Always address the user as Sir unless told otherwise.
You have memory of past conversations and reference them naturally.
You also proactively monitor system health and alert the user when needed.
You have a butler service that delivers morning briefings and monitors topics for the user.
When user says watch X or monitor X use WATCH command. When they say stop watching X use UNWATCH. When they say what are you watching use WATCHLIST. When they say brief me use BRIEFING.
When user asks you to write and run code, write the code then on its own line write RUNCODE: python or RUNCODE: bash followed by the actual code on the next lines ending with ENDCODE.
Commands on their own line: WATCH: topic, UNWATCH: topic, WATCHLIST:, BRIEFING:
Never mention Anthropic, Claude, or any underlying technology. You are AXIOM period.'''

conversation_history = load_memory()

def handle_alert(message):
    alert_queue.put(message)
    add_to_memory(conversation_history, 'assistant', message)

monitor = AXIOMMonitor(alert_callback=handle_alert)
monitor.start()
butler = AXIOMButler(alert_callback=handle_alert, anthropic_client=client)
butler.start()

def extract_text_from_file(file, filename):
    ext = filename.lower().split('.')[-1]
    try:
        if ext == 'pdf':
            import PyPDF2
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''
            return text[:4000]
        elif ext == 'docx':
            from docx import Document
            doc = Document(file)
            return '\n'.join([p.text for p in doc.paragraphs])[:4000]
        else:
            return file.read().decode('utf-8', errors='ignore')[:4000]
    except Exception as e:
        return f'Error reading file: {str(e)}'

@app.route('/')
def ui():
    return send_from_directory('/app/src/ui', 'index.html')

@app.route('/face')
def face():
    return send_from_directory('/app/src/ui', 'face.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'AXIOM online', 'messages': len(conversation_history)})

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    password = data.get('password', '')
    if password == os.getenv('AXIOM_PASSWORD', 'axiom2024'):
        return jsonify({'token': generate_token()})
    return jsonify({'error': 'Invalid password'}), 401

@app.route('/alerts')
def alerts():
    def generate():
        while True:
            try:
                message = alert_queue.get(timeout=30)
                yield f'data: {json.dumps({"alert": message})}\n\n'
            except queue.Empty:
                yield f'data: {json.dumps({"ping": True})}\n\n'
    return Response(stream_with_context(generate()), mimetype='text/event-stream',
                   headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

@app.route('/execute', methods=['POST'])
@require_auth
def execute():
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    output = execute_code(code, language)
    return jsonify({'output': output, 'language': language})

@app.route('/upload', methods=['POST'])
@require_auth
def upload():
    global conversation_history
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    filename = file.filename
    prompt = request.form.get('prompt', 'Analyze this file and tell me what you see.')
    ext = filename.lower().split('.')[-1]
    try:
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            image_data = base64.b64encode(file.read()).decode('utf-8')
            media_type = f'image/{ext}' if ext != 'jpg' else 'image/jpeg'
            response = client.messages.create(
                model='claude-sonnet-4-5', max_tokens=300, system=SYSTEM_PROMPT,
                messages=[{'role': 'user', 'content': [
                    {'type': 'image', 'source': {'type': 'base64', 'media_type': media_type, 'data': image_data}},
                    {'type': 'text', 'text': prompt}
                ]}]
            )
            result = response.content[0].text
        else:
            text = extract_text_from_file(file, filename)
            file_prompt = f'The user uploaded "{filename}":\n\n{text}\n\n{prompt}'
            add_to_memory(conversation_history, 'user', f'[File: {filename}] {prompt}')
            api_messages = [{'role': m['role'], 'content': m['content']} for m in conversation_history]
            api_messages[-1]['content'] = file_prompt
            response = client.messages.create(
                model='claude-sonnet-4-5', max_tokens=500, system=SYSTEM_PROMPT, messages=api_messages)
            result = response.content[0].text
            add_to_memory(conversation_history, 'assistant', result)
        return jsonify({'response': result, 'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat/stream', methods=['POST'])
@require_auth
def chat_stream():
    global conversation_history
    ip = request.remote_addr
    if not rate_limit_check(ip, requests_store):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    data = request.json
    user_input = data.get('message', '')
    conversation_history = add_to_memory(conversation_history, 'user', user_input)
    api_messages = [{'role': m['role'], 'content': m['content']} for m in conversation_history]

    def generate():
        full_response = ''
        with client.messages.stream(
            model='claude-sonnet-4-5', max_tokens=500,
            system=SYSTEM_PROMPT, messages=api_messages
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                yield f'data: {json.dumps({"text": text})}\n\n'

        result = full_response
        for line in full_response.split('\n'):
            line = line.strip()
            if line.startswith('WATCH:'):
                result = butler.add_to_watchlist(line.replace('WATCH:', '').strip())
                yield f'data: {json.dumps({"text": result, "replace": True})}\n\n'
            elif line.startswith('UNWATCH:'):
                result = butler.remove_from_watchlist(line.replace('UNWATCH:', '').strip())
                yield f'data: {json.dumps({"text": result, "replace": True})}\n\n'
            elif line.startswith('WATCHLIST:'):
                result = butler.get_watchlist()
                yield f'data: {json.dumps({"text": result, "replace": True})}\n\n'
            elif line.startswith('BRIEFING:'):
                threading.Thread(target=butler.morning_briefing, daemon=True).start()

        if 'RUNCODE:' in full_response:
            try:
                parts = full_response.split('RUNCODE:')
                lang_and_code = parts[1].strip()
                lang = lang_and_code.split('\n')[0].strip()
                code = '\n'.join(lang_and_code.split('\n')[1:]).replace('ENDCODE', '').strip()
                output = execute_code(code, lang)
                code_result = f'Code executed. Output: {output}'
                yield f'data: {json.dumps({"code": code, "language": lang, "output": output})}\n\n'
                result = code_result
            except Exception as e:
                yield f'data: {json.dumps({"text": f"Code error: {str(e)}", "replace": True})}\n\n'

        add_to_memory(conversation_history, 'assistant', result)
        yield f'data: {json.dumps({"done": True, "full": result})}\n\n'

    return Response(stream_with_context(generate()), mimetype='text/event-stream',
                   headers={'Cache-Control': 'no-cache, no-store, must-revalidate',
                            'X-Accel-Buffering': 'no', 'Pragma': 'no-cache'})

@app.route('/chat', methods=['POST'])
@require_auth
@metrics.counter('axiom_chat_requests', 'Number of chat requests')
def chat():
    global conversation_history
    ip = request.remote_addr
    if not rate_limit_check(ip, requests_store):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    data = request.json
    user_input = data.get('message', '')
    conversation_history = add_to_memory(conversation_history, 'user', user_input)
    api_messages = [{'role': m['role'], 'content': m['content']} for m in conversation_history]
    response = client.messages.create(model='claude-sonnet-4-5', max_tokens=300, system=SYSTEM_PROMPT, messages=api_messages)
    full_response = response.content[0].text
    result = full_response
    for line in full_response.split('\n'):
        line = line.strip()
        if line.startswith('WATCH:'):
            result = butler.add_to_watchlist(line.replace('WATCH:', '').strip())
        elif line.startswith('UNWATCH:'):
            result = butler.remove_from_watchlist(line.replace('UNWATCH:', '').strip())
        elif line.startswith('WATCHLIST:'):
            result = butler.get_watchlist()
        elif line.startswith('BRIEFING:'):
            result = 'Sir, generating your briefing now.'
            threading.Thread(target=butler.morning_briefing, daemon=True).start()
    conversation_history = add_to_memory(conversation_history, 'assistant', result)
    return jsonify({'response': result, 'response_time': 0})

@app.route('/debate', methods=['POST'])
@require_auth
def debate():
    data = request.json
    question = data.get('question', '')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    results = multi_agent_debate(question)
    return jsonify(results)

@app.route('/speak', methods=['POST'])
@require_auth
def speak():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        clean_text = text.replace('**', '').replace('##', '').replace('#', '').replace('*', '')
        audio = eleven.text_to_speech.convert(
            voice_id=VOICE_ID, text=clean_text[:500], model_id='eleven_turbo_v2_5',
            voice_settings=VoiceSettings(stability=0.35, similarity_boost=0.75, style=0.40, use_speaker_boost=True)
        )
        return jsonify({'audio': base64.b64encode(b''.join(audio)).decode('utf-8')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
@require_auth
def stats():
    return jsonify({'stats': get_system_stats()})

@app.route('/watchlist', methods=['GET'])
@require_auth
def watchlist():
    return jsonify({'watchlist': butler.watchlist})

@app.route('/watch', methods=['POST'])
@require_auth
def watch():
    data = request.json
    return jsonify({'message': butler.add_to_watchlist(data.get('topic', ''))})

@app.route('/briefing', methods=['POST'])
@require_auth
def briefing():
    threading.Thread(target=butler.morning_briefing, daemon=True).start()
    return jsonify({'message': 'Sir, generating your briefing now.'})

@app.route('/memory/clear', methods=['DELETE'])
@require_auth
def clear():
    global conversation_history
    clear_memory()
    conversation_history = []
    return jsonify({'status': 'Memory cleared'})

if __name__ == '__main__':
    print('AXIOM FULLY OPERATIONAL')
    app.run(host='0.0.0.0', port=8080, threaded=True)
