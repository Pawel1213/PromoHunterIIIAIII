# Файл: get_session.py
import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")

if not api_id or not api_hash:
    print("❌ Помилка: Не знайдено API_ID або API_HASH у файлі .env")
else:
    print("🔐 Вхід для генерації рядка сесії...")
    # Ми використовуємо StringSession
    with TelegramClient(StringSession(), int(api_id), api_hash) as client:
        print("\n👇 ВАШ РЯДОК СЕСІЇ (Скопіюйте все від початку до кінця!): 👇\n")
        print(client.session.save())
        print("\n👆 Скопіюйте цей довгий код і додайте його в .env як TG_SESSION_STRING")