import os

# Шлях до файлу, який ми хочемо створити
path = os.path.join("src", "database.py")

# Код, який має бути всередині database.py
code_content = """import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Завантажуємо ключі
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Створюємо клієнта
if not url or not key:
    print("❌ ПОМИЛКА: Не знайдено SUPABASE_URL або KEY в .env файлі!")
    supabase = None
else:
    supabase: Client = create_client(url, key)

def save_bonus(casino_name: str, bonus_offer: str, wagering: str):
    if not supabase:
        print("❌ Немає з'єднання з базою.")
        return

    data = {
        "casino_name": casino_name,
        "bonus_offer": bonus_offer,
        "wagering": wagering
    }

    try:
        response = supabase.table("bonuses").insert(data).execute()
        print(f"✅ Збережено в базу: {casino_name}")
        return response
    except Exception as e:
        print(f"❌ Помилка запису в БД: {e}")
"""

print(f"🔨 Створюю файл {path}...")

try:
    with open(path, "w", encoding="utf-8") as f:
        f.write(code_content)
    print("✅ ГОТОВО! Файл database.py успішно створено всередині папки src.")
except Exception as e:
    print(f"❌ Не вдалося створити файл: {e}")

# Перевірка на всяк випадок файлу __init__.py (у логах він виглядав дивно)
init_path = os.path.join("src", "__init__.py")
if not os.path.exists(init_path):
    with open(init_path, "w") as f:
        pass
    print("✅ Також відновлено файл __init__.py")