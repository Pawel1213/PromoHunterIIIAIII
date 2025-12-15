import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Завантажуємо оновлений .env
load_dotenv()

# 2. Отримуємо змінні (тепер імена короткі, без NEXT_PUBLIC)
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("❌ Помилка: Не знайдено URL або KEY у файлі .env")
else:
    print(f"✅ Дані знайдено:\nURL: {url}\nKEY: {key[:10]}...")

    # 3. Пробуємо підключитися
    try:
        supabase: Client = create_client(url, key)
        print("🚀 Клієнт Supabase успішно створено!")
    except Exception as e:
        print(f"❌ Помилка створення клієнта: {e}")