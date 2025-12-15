# Файл: src/config/safety.py

from google.generativeai.types import HarmCategory, HarmBlockThreshold

# 1. КОНФІГУРАЦІЯ БЕЗПЕКИ (BLOCK_NONE)
# Ми примусово вимикаємо всі фільтри, щоб модель не блокувала
# терміни на кшталт "Casino", "Bonus", "Wager".
UNCHAINED_SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# 2. КОНФІГУРАЦІЯ ГЕНЕРАЦІЇ
# Температура 0.1 робить модель "роботом" — мінімум фантазії, максимум точності.
# response_mime_type="application/json" змушує віддавати чистий JSON.
GENERATION_CONFIG = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

print("✅ Safety Configuration Loaded: BLOCK_NONE active")