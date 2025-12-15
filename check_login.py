# Файл: check_login.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("--- 🕵️‍♂️ ДІАГНОСТИКА UPWORK ---")

# 1. Перевіряємо, чи бачить Python файл .env
cookie = os.getenv("MY_COOKIE")
user_agent = os.getenv("MY_USER_AGENT")

if not cookie:
    print("❌ ПОМИЛКА: Змінна MY_COOKIE пуста! Перевірте файл .env")
    exit()

print(f"✅ Cookie знайдено! Довжина: {len(cookie)} символів.")

# Перевірка на "розірваний" рядок
if len(cookie) < 500:
    print("⚠️ УВАГА: Cookie підозріло короткий. Можливо, він обрізаний?")
else:
    print("👌 Довжина виглядає нормально.")

# 2. Робимо тестовий запит
url = "https://www.upwork.com/ab/feed/jobs/rss?q=python"

headers = {
    "User-Agent": user_agent,
    "Cookie": cookie
}

print(f"\n📡 Пробую зайти на Upwork...")

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"📊 Статус відповіді: {response.status_code}")

    if response.status_code == 200:
        print("🎉 УРА! Авторизація пройшла успішно! Бот має працювати.")
        print("Якщо бот не працює - значить проблема в коді freelance.py, а не в ключах.")
    elif response.status_code == 403:
        print("⛔ 403 Forbidden.")
        print("Це означає, що Upwork відхилив ці Cookies.")
        print("Рішення: Треба знову зайти в браузер (Network -> Headers) і скопіювати НОВІ Cookies.")
    else:
        print(f"⚠️ Інша помилка. Текст відповіді: {response.text[:100]}")

except Exception as e:
    print(f"❌ Помилка з'єднання: {e}")