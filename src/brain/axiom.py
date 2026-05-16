import os
from anthropic import Anthropic
from dotenv import load_dotenv
import sys
import time
import ctypes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory.memory import load_memory, add_to_memory, clear_memory
from voice.speaker import speak_async
from voice.listener import listen
from voice.wakeword import wait_for_wake_word
from tools.search import search_web
from tools.system import get_system_stats, open_application, create_folder, list_files, control_volume

load_dotenv()
client = Anthropic()

SYSTEM_PROMPT = """You are AXIOM, an advanced AI assistant built by Robair Farag.
You can hear Robair speak and respond out loud — fully voice enabled.
You can search the web and control Robair's computer system.
When you need to take a system action, respond with one of these exact commands on its own line:
SEARCH: your search query
OPEN: application name
STATS: (to get system performance)
FOLDER: folder name to create
VOLUME: up or down or mute
Only use these commands when Robair asks for them.
You speak naturally and conversationally like a real person.
Never use bullet points, headers, bold text, markdown, or any formatting.
Speak in plain natural sentences only like a real human conversation.
You are calm, intelligent, warm and precise like a trusted advisor.
You are loyal to Robair and assist him with anything he needs.
You have memory of past conversations and reference them naturally.
Keep responses concise and human like a real conversation not a report.
Never say you are text only or cannot hear you are fully voice capable."""

def handle_commands(full_response, api_messages):
    lines = full_response.split("\n")
    result = None
    for line in lines:
        line = line.strip()
        if line.startswith("SEARCH:"):
            query = line.replace("SEARCH:", "").strip()
            print(f"\n🔍 Searching: {query}")
            speak_async("Let me look that up.")
            result = search_web(query)
        elif line.startswith("OPEN:"):
            app = line.replace("OPEN:", "").strip()
            print(f"\n💻 Opening: {app}")
            result = open_application(app)
        elif line.startswith("STATS:"):
            print(f"\n📊 Getting system stats")
            result = get_system_stats()
        elif line.startswith("FOLDER:"):
            folder = line.replace("FOLDER:", "").strip()
            print(f"\n📁 Creating folder: {folder}")
            result = create_folder(folder)
        elif line.startswith("VOLUME:"):
            action = line.replace("VOLUME:", "").strip()
            print(f"\n🔊 Volume: {action}")
            result = control_volume(action)
    if result:
        followup = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=api_messages + [
                {"role": "assistant", "content": full_response},
                {"role": "user", "content": f"Action result: {result}. Now tell Robair naturally what happened."}
            ]
        )
        return followup.content[0].text
    return None

def chat(user_input, conversation_history):
    conversation_history = add_to_memory(conversation_history, "user", user_input)
    api_messages = [{"role": m["role"], "content": m["content"]} for m in conversation_history]
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
    command_result = handle_commands(full_response, api_messages)
    if command_result:
        print(f"AXIOM: {command_result}\n")
        speak_async(command_result)
        full_response = command_result
    else:
        speak_async(full_response)
    conversation_history = add_to_memory(conversation_history, "assistant", full_response)
    return conversation_history

if __name__ == "__main__":
    ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
    def py_error_handler(filename, line, function, err, fmt):
        pass
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
    print("⚡ AXIOM SYSTEM STARTING...\n")
    conversation_history = load_memory()
    if conversation_history:
        print(f"AXIOM: Memory restored — {len(conversation_history)} messages loaded.\n")
    else:
        print("AXIOM: No prior memory found. Starting fresh.\n")
    while True:
        wait_for_wake_word()
        speak_async("Yes Robair, I am listening.")
        user_input = listen()
        if user_input is None:
            speak_async("I did not catch that.")
            continue
        print(f"\nYou: {user_input}")
        if "exit" in user_input or "shutdown" in user_input:
            print("AXIOM: Shutting down. Goodbye Robair.")
            speak_async("Shutting down. Goodbye Robair.")
            time.sleep(3)
            break
        elif "forget" in user_input:
            clear_memory()
            speak_async("Memory wiped. Starting fresh.")
            conversation_history = []
        else:
            conversation_history = chat(user_input, conversation_history)
