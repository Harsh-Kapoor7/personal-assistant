from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    azure_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
    azure_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

    # Optional STT via OpenAI Whisper
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Optional TTS via ElevenLabs
    elevenlabs_api_key: str = os.getenv("ELEVENLABS_API_KEY", "")
    elevenlabs_voice_id: str = os.getenv("ELEVENLABS_VOICE_ID", "")

    app_data_dir: str = os.getenv("APP_DATA_DIR", "./app_data")
    checkin_minutes: int = int(os.getenv("CHECKIN_MINUTES", "60"))
    idle_soft_min: int = int(os.getenv("IDLE_SOFT_MIN", "20"))
    idle_firm_min: int = int(os.getenv("IDLE_FIRM_MIN", "30"))
    idle_enforce_min: int = int(os.getenv("IDLE_ENFORCE_MIN", "45"))
    default_gym_slot: str = os.getenv("DEFAULT_GYM_SLOT", "19:00-20:00")
    timezone: str = os.getenv("LOCAL_TIMEZONE", "Asia/Kolkata")

settings = Settings()

# Ensure data folders
os.makedirs(settings.app_data_dir, exist_ok=True)
os.makedirs(os.path.join(settings.app_data_dir, "logs"), exist_ok=True)