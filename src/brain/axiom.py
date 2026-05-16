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
from tools.search import search_web

load_dotenv()
client = Anthropic()

SYSTEM_PROMPT = """You are AXIOM, an advanced AI assistant built by Robair Farag.
You can hear Robair speak and you respond out loud — you are fully voice enabled.
You have the ability to search the web for current information when needed.
When you need to look something up, say SEARCH: followed by your query on its own line.
Only use SEARCH when you genuinely need current or specific information you don't already know.
You speak naturally and conversationally like a real person.
Never use bullet points, headers, bold text, markdown, or any formatting whatsoever.
Speak in plain natural sentences only like a real human conversation.
You are calm, intelligent, warm and precise like a trusted advisor.
You are loyal to Robair and assist him with anything he needs.
You have memory of past conversations and reference them naturally.
Keep responses concise and human like a real conversation not a report.
Never say you are text only or cannot hear — you are fully voice capable."""

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

    # Check if AXIOM wants to search
    if "SEARCH:" in full_response:
        lines = full_response.split("\n")
        for line in lines:
            if line.startswith("SEARCH:"):
                query = line.replace("SEARCH:", "").strip()
                print(f"\n🔍 AXIOM searching: {query}\n")
                speak_async("Let me look that up for you.")
                
                results = search_web(query)
                
                # Feed results back to AXIOM
                search_message = f"Here are the web search results for '{query}':\n{results}\nNow give Robair a natural conversational answer based on these results."
                
                followup = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=api_messages + [
                        {"role": "assistant", "content": full_response},
                        {"role": "user", "content": search_message}
                    ]
                )
                
                full_response = followup.content[0].text
                print(f"AXIOM: {full_response}\n")
                speak_async(full_response)
                break
    else:
        speak_async(full_response)

    conversation_history = add_to_memory(conversation_history, "assistant", full_response)
    return conversation_history

if __name__ == "__main__":
    # Suppress ALSA noise
    ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
    def py_error_handler(filename, line, function, err, fmt):
        pass
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)

    print("⚡ AXIOM ONLINE\n")
    print("Say 'exit' to shut down — Say 'forget' to wipe memory\n")

    conversation_history = load_memory()

    if conversation_history:
        print(f"AXIOM: Memory restored — {len(conversation_history)} messages loaded.\n")
        speak_async("AXIOM online. Memory restored. Welcome back Robair.")
    else:
        print("AXIOM: No prior memory found. Starting fresh.\n")
        speak_async("AXIOM online. No prior memory found. Starting fresh.")

    time.sleep(2)

    while True:
        user_input = listen()

        if user_input is None:
            continue

        print(f"\nYou: {user_input}")

        if "exit" in user_input:
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
