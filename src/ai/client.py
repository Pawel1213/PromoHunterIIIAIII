# Файл: src/ai/client.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.config.safety import UNCHAINED_SAFETY_SETTINGS, GENERATION_CONFIG

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file!")

genai.configure(api_key=api_key)


def get_model(use_advanced=False):
    """
    Фабрика моделей.
    Використовуємо Gemini 2.0 Flash, оскільки вона офіційно доступна
    для вашого платного акаунту.
    """
    # ТОЧНА НАЗВА З ВАШОГО СПИСКУ
    model_name = "gemini-2.0-flash"

    print(f"🤖 Loading Model: {model_name}")

    model = genai.GenerativeModel(
        model_name=model_name,
        safety_settings=UNCHAINED_SAFETY_SETTINGS,
        generation_config=GENERATION_CONFIG,
        system_instruction="You are a JSON-only data extraction engine."
    )
    return model