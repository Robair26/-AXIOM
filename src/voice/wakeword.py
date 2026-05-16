import speech_recognition as sr

recognizer = sr.Recognizer()

WAKE_WORDS = ["hey axiom", "axiom", "hey axium", "hey ax"]

def wait_for_wake_word():
    """Wait until AXIOM hears his name"""
    print("💤 AXIOM sleeping — say 'Hey AXIOM' to wake up...\n")
    
    while True:
        try:
            with sr.Microphone(device_index=11) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                text = recognizer.recognize_google(audio).lower()
                
                for wake_word in WAKE_WORDS:
                    if wake_word in text:
                        print("⚡ AXIOM ACTIVATED\n")
                        return True
                        
        except:
            continue
