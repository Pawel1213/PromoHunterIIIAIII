# Файл: check_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Завантаження ключа
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Ключ не знайдено в .env")
else:
    print(f"🔑 Ключ знайдено: {api_key[:5]}...*****")
    genai.configure(api_key=api_key)

    print("\n📡 Запитую у Google список доступних моделей...")
    try:
        count = 0
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" ✅ Доступна модель: {m.name}")
                count += 1
        
        if count == 0:
            print("⚠️ Список пустий. Можливо, API не активовано для цього проєкту.")
            
    except Exception as e:
        print(f"❌ Помилка при отриманні списку: {e}")