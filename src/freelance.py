import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

# Завантаження змінних
load_dotenv()

# --- ОТРИМАННЯ КЛЮЧІВ ---
# Читаємо змінні середовища
api_id_raw = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")
session_string = os.getenv("TG_SESSION_STRING")

print(f"DEBUG: API_ID found? {bool(api_id_raw)}")
print(f"DEBUG: API_HASH found? {bool(api_hash)}")
print(f"DEBUG: SESSION found? {bool(session_string)}")

# Конвертація ID в число
try:
    if api_id_raw:
        api_id = int(api_id_raw)
    else:
        print("❌ CRITICAL: TG_API_ID не знайдено!")
        api_id = None
except ValueError:
    print("❌ CRITICAL: TG_API_ID має бути числом!")
    api_id = None

# --- ІНІЦІАЛІЗАЦІЯ КЛІЄНТА ---
# Пріоритет: StringSession (для хмари) -> Файл (локально)
if session_string:
    print("☁️ Хмарний режим: Стартую через StringSession...")
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
else:
    print("📂 Локальний режим: Шукаю файл .session...")
    client = TelegramClient('anon', api_id, api_hash)


# --- ФУНКЦІЯ ---
def get_open_jobs(limit=5, keyword=None):
    channels = ['@djinni_official', '@catwork', '@freelance_ua', '@python_jobs', '@remote_ua']
    results = []

    async def main():
        try:
            if not api_id or not api_hash:
                print("❌ Неможливо запустити Telethon: немає ключів!")
                return

            print("🔄 Підключення до Telegram...")
            await client.connect()

            if not await client.is_user_authorized():
                print("❌ Сесія не авторизована! Потрібен новий String Session.")
                return

            print("✅ Telethon підключено!")

            for channel in channels:
                try:
                    async for message in client.iter_messages(channel, limit=limit):
                        if message.text:
                            text = message.text
                            # Фільтрація
                            if keyword:
                                if isinstance(keyword, list):
                                    if not any(k.lower() in text.lower() for k in keyword):
                                        continue
                                elif keyword.lower() not in text.lower():
                                    continue

                            lines = text.split('\n')
                            title = lines[0][:100] + "..." if len(lines[0]) > 100 else lines[0]
                            link = f"https://t.me/{message.chat.username}/{message.id}" if message.chat.username else "#"

                            results.append({
                                'source': channel,
                                'title': title.replace('*', '').replace('_', ''),
                                'link': link,
                                'description': text[:200] + "..."
                            })
                except Exception as e:
                    print(f"⚠️ Помилка каналу {channel}: {e}")

        except Exception as e:
            print(f"❌ Помилка Telethon: {e}")
        finally:
            await client.disconnect()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    return results