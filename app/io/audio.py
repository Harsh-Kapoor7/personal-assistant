from __future__ import annotations
import sys

# Minimal audio I/O helpers with graceful fallbacks to text input/output

try:
    import sounddevice as sd
    import numpy as np
    from scipy.io.wavfile import write as wav_write
except Exception:
    sd = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    import whisper
    whisper_model = whisper.load_model("base")
except Exception:
    whisper = None
    whisper_model = None

from app.config import settings

# === TTS ===
_engine = None

def tts_say(text: str):
    """Speak text via pyttsx3 fallback. In Phase-2 you can switch to ElevenLabs easily."""
    global _engine
    print(f"\nAssistant: {text}\n")
    if pyttsx3 is None:
        return
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty('rate', 185)
    _engine.say(text)
    _engine.runAndWait()

# === STT Placeholder ===
# In Phase-1, we default to text input for stability. You can wire Whisper in later.

def listen_once(prompt: str = "You:") -> str:
    if sd is None or whisper_model is None:
        try:
            inp = input(f"{prompt} ")
            return inp.strip()
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(0)
    else:
        try:
            fs = 16000  # Sample rate
            duration = 5  # seconds
            print(f"{prompt} (Recording for {duration} seconds...)")
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()
            wav_write("input.wav", fs, recording)
            result = whisper_model.transcribe("input.wav")
            return result["text"].strip()
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(0)
        except Exception as e:
            print(f"Error during transcription: {e}")
            try:
                inp = input(f"{prompt} ")
                return inp.strip()
            except KeyboardInterrupt:
                print("\nExiting.")
                sys.exit(0)