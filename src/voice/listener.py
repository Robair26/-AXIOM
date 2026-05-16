import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

def listen():
    """AXIOM listens for your voice"""
    with sr.Microphone(device_index=11) as source:
        print("AXIOM is listening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("AXIOM: I didn't catch that.")
            return None
        except sr.RequestError:
            print("AXIOM: Voice service unavailable.")
            return None
