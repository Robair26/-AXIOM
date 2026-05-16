import os
import pygame
import threading
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from dotenv import load_dotenv
import tempfile

load_dotenv()

# Initialize ElevenLabs client
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Brian — natural, warm, conversational American male voice
VOICE_ID = "nPczCjzI2devNBz1zQrb"

def speak(text):
    """AXIOM speaks naturally like a real person"""
    # Clean markdown
    clean_text = text.replace("**", "").replace("##", "").replace("#", "").replace("---", "").replace("*", "").replace("•", "")

    # Generate audio from ElevenLabs
    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=clean_text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.35,        # Lower = more expressive and natural
            similarity_boost=0.75, # Keeps the voice consistent
            style=0.40,            # Adds natural human style and emotion
            use_speaker_boost=True
        )
    )

    # Save to temp file and play
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        for chunk in audio:
            f.write(chunk)
        temp_path = f.name

    pygame.mixer.music.load(temp_path)
    pygame.mixer.music.play()

    # Wait for audio to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def speak_async(text):
    """Speak without blocking the terminal"""
    thread = threading.Thread(target=speak, args=(text,))
    thread.daemon = True
    thread.start()
