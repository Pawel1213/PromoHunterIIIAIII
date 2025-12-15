# Файл: src/database.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Завантажуємо ключі
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Створюємо клієнта
supabase: Client = create_client(url, key)

def save_bonus(casino_name: str, bonus_offer: str, wagering: str):
    """
    Зберігає один бонус у базу даних Supabase.
    """
    data = {
        "casino_name": casino_name,
        "bonus_offer": bonus_offer,
        "wagering": wagering
    }

    # Виконуємо вставку (insert) в таблицю 'bonuses'
    try:
        response = supabase.table("bonuses").insert(data).execute()
        print(f"✅ Збережено в базу: {casino_name}")
        return response
    except Exception as e:
        print(f"❌ Помилка запису в БД: {e}")