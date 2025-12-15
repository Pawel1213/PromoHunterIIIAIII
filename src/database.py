# Файл: src/database.py
import os
import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)


def save_bonus(casino_name: str, bonus_offer: str, wagering: str, link: str):
    """
    Робить UPSERT:
    - Якщо казино нове -> створює запис.
    - Якщо казино вже є -> оновлює бонус, лінк і час (created_at).
    """

    # Отримуємо поточний час, щоб помітити, коли ми останній раз оновлювали запис
    current_time = datetime.datetime.now().isoformat()

    data = {
        "casino_name": casino_name,
        "bonus_offer": bonus_offer,
        "wagering": wagering,
        "link": link,
        "created_at": current_time  # Оновлюємо дату перевірки
    }

    try:
        # on_conflict="casino_name" означає: "Якщо така назва є, не створюй нову, а онови існуючу"
        response = supabase.table("bonuses").upsert(data, on_conflict="casino_name").execute()
        print(f"✅ Дані оновлено/додано: {casino_name}")
        return response
    except Exception as e:
        print(f"❌ Помилка запису в БД: {e}")