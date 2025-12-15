import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# --- ОТРИМАННЯ КЛЮЧІВ (ВИПРАВЛЕНО НАЗВИ) ---
# У Railway змінні беруться напряму з os.environ, load_dotenv() не потрібен
api_id_raw = os.getenv("TG_API_ID", "0")
api_hash = os.getenv("TG_API_HASH", "")
session_string = os.getenv("TG_SESSION_STRING", "")

# Логування для перевірки (не показує самі ключі, тільки статус)
print(f"DEBUG: TG_API_ID (raw): {api_id_raw}")
print(f"DEBUG: TG_API_HASH exists? {bool(api_hash)}")
print(f"DEBUG: TG_SESSION_STRING exists? {bool(session_string)}")

# Конвертація ID в число
try:
    api_id = int(api_id_raw)
    if api_id == 0:
        raise ValueError("TG_API_ID = 0")
except (ValueError, TypeError) as e:
    print(f"❌ ERROR: TG_API_ID має бути числом! Перевірте змінні. ({e})")
    api_id = 0

# Перевірка наявності обов'язкових даних
if not api_id or not api_hash:
    print("❌ CRITICAL: TG_API_ID або TG_API_HASH відсутні!")

# --- ІНІЦІАЛІЗАЦІЯ КЛІЄНТА ---
# Логіка: Якщо є StringSession -> Хмара, інакше -> Файл
if session_string:
    print("☁️ Хмарний режим: Стартую через StringSession...")
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
else:
    print("📂 Локальний режим: Шукаю файл .session...")
    client = TelegramClient('anon', api_id, api_hash)


# --- ФУНКЦІЯ ПАРСИНГУ ---
def get_open_jobs(limit=5, keyword=None):
    channels = ['@djinni_official', '@catwork', '@freelance_ua', '@python_jobs', '@remote_ua']
    results = []

    async def main():
        try:
            # Перевірка перед стартом
            if not api_id or api_id == 0 or not api_hash:
                print("❌ Неможливо запустити Telethon: відсутні API_ID або API_HASH")
                return

            print("🔄 Підключення до Telegram...")
            await client.connect()

            if not await client.is_user_authorized():
                print("❌ Сесія не авторизована! Потрібен свіжий TG_SESSION_STRING.")
                return

            print("✅ Telethon успішно підключено!")

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

    # Для Railway/prod-середовища краще використовувати існуючий event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(main())
    return results
