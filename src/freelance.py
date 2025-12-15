# Файл: src/freelance.py (ФІНАЛЬНИЙ: ПІДТРИМКА STRING SESSION)
import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession  # Важливий імпорт
from dotenv import load_dotenv
import google.generativeai as genai
import textwrap
from pathlib import Path

# --- ЗАВАНТАЖЕННЯ .ENV ---
base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / '.env'
load_dotenv(dotenv_path=env_path)

# Отримуємо ключі
API_ID = os.getenv("TG_API_ID")
API_HASH = os.getenv("TG_API_HASH")
SESSION_STRING = os.getenv("TG_SESSION_STRING")  # Читаємо довгий код
CHANNELS_STR = os.getenv("CHANNELS_TO_PARSE", "@djinni_official")
CHANNELS = CHANNELS_STR.split(',')
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Налаштування AI
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    ai_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    ai_model = None

# --- ГОЛОВНА ЛОГІКА АВТОРИЗАЦІЇ ---
if API_ID:
    API_ID = int(API_ID)

# Тут магія: якщо є рядок сесії (для сервера), беремо його.
# Якщо ні (локально), шукаємо файл 'anon.session'.
if SESSION_STRING:
    print("✅ Використовую String Session з .env (Хмарний режим)")
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
else:
    print("📂 Використовую файлову сесію anon.session (Локальний режим)")
    client = TelegramClient('anon', API_ID, API_HASH)


# --- ФУНКЦІЯ ОЦІНКИ РЕЛЕВАНТНОСТІ (AI) ---
def is_relevant_by_ai(job_description, keywords):
    """Використовує Gemini для фільтрації."""
    if not ai_model or not keywords:
        return True

    keyword_list_str = ", ".join([f"'{kw.strip()}'" for kw in keywords])

    prompt = f"""
    Проаналізуй текст вакансії.
    Чи відповідає він хоча б одному з цих ключових слів/тем: {keyword_list_str}?
    Текст: "{job_description[:600]}"
    Відповідай тільки 'ТАК' або 'НІ'.
    """

    try:
        response = ai_model.generate_content(prompt)
        return "ТАК" in response.text.upper()
    except:
        return True


async def fetch_telegram_jobs(limit=5, keywords=None):
    """Асинхронна функція для отримання повідомлень з реальних каналів."""
    jobs_list = []

    try:
        # Підключення
        await client.connect()

        # Перевірка авторизації
        if not await client.is_user_authorized():
            print("❌ ПОМИЛКА: Клієнт не авторизований! Перевірте TG_SESSION_STRING.")
            return []

        # Проходимо по списку каналів
        for channel in CHANNELS:
            try:
                messages = await client.get_messages(channel, limit=10)

                for msg in messages:
                    if not msg.text or len(msg.text) < 50:
                        continue

                    if keywords:
                        if not is_relevant_by_ai(msg.text, keywords):
                            continue

                    if msg.chat.username:
                        link = f"https://t.me/{msg.chat.username}/{msg.id}"
                    else:
                        link = "#"

                    clean_desc = msg.text.replace('**', '').replace('__', '')
                    short_desc = textwrap.shorten(clean_desc, width=200, placeholder="...")

                    title = clean_desc.split('\n')[0][:60]
                    if not title.strip():
                        title = "🔥 Гаряча вакансія"

                    jobs_list.append({
                        "source": f"TG: {channel}",
                        "title": title,
                        "link": link,
                        "description": short_desc
                    })

                    if len(jobs_list) >= limit:
                        break
            except Exception as e:
                continue

            if len(jobs_list) >= limit:
                break

    except Exception as e:
        print(f"Global Telethon Error: {e}")
        return []

    return jobs_list


# --- ОБГОРТКА ДЛЯ ВИКЛИКУ З БОТА ---
def get_open_jobs(limit=5, keyword=None):
    if isinstance(keyword, str):
        keywords = [kw.strip() for kw in keyword.replace('/', ',').replace(',', ' ').split() if kw.strip()]
    elif isinstance(keyword, list):
        keywords = keyword
    else:
        keywords = None

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(fetch_telegram_jobs(limit, keywords))
    loop.close()

    if not result:
        return []

    return result


# --- БЛОК ТЕСТУВАННЯ ---
if __name__ == "__main__":
    print("🔬 Тестування з'єднання...")
    with client:
        client.loop.run_until_complete(client.get_me())
        print("✅ Успішно! Telethon працює коректно.")