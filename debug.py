# Файл: debug.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Завантажуємо дані
COOKIE = os.getenv("MY_COOKIE")
USER_AGENT = os.getenv("MY_USER_AGENT")
URL = "https://www.upwork.com/ab/feed/jobs/rss?q=python&sort=recency"

print("--- ДІАГНОСТИКА ---")

# 1. Перевірка змінних
if not COOKIE:
    print("❌ ПОМИЛКА: Cookie не знайдено в .env!")
    exit()
else:
    print(f"✅ Cookie завантажено (Довжина: {len(COOKIE)} символів)")
    print(f"   Початок: {COOKIE[:30]}...")

if not USER_AGENT:
    print("❌ ПОМИЛКА: User-Agent не знайдено!")
    exit()

# 2. Спроба запиту
headers = {
    "User-Agent": USER_AGENT,
    "Cookie": COOKIE
}

print(f"\n📡 Роблю запит до: {URL}...")

try:
    response = requests.get(URL, headers=headers, timeout=10)

    print(f"📊 Статус код: {response.status_code}")

    if response.status_code == 200:
        print("🎉 УСПІХ! Upwork пропустив запит.")
        print("Ось шматочок відповіді:")
        print(response.text[:200])
    elif response.status_code == 403:
        print("⛔ 403 FORBIDDEN. Upwork все ще блокує.")
        print("Причини: ")
        print("1. Cookie неправильно скопійовано (має бути 1 рядок).")
        print("2. User-Agent не співпадає з тим, що в браузері.")
        print("3. Треба оновити Cookie (вони живуть недовго).")
    else:
        print(f"⚠️ Інша помилка: {response.status_code}")
        print(response.text[:500])

except Exception as e:
    print(f"❌ Критична помилка з'єднання: {e}")