# Файл: src/notifier.py
import os
import telebot
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_new_bonuses():
    print("🔔 Шукаю нові бонуси...")

    try:
        # Тепер ми беремо найсвіжіші за часом (created_at), навіть якщо це старий запис, який щойно оновився
        response = supabase.table("bonuses").select("*").order("created_at", desc=True).limit(10).execute()
        bonuses = response.data
    except Exception:
        return

    if not bonuses:
        print("📭 Пусто.")
        return

    message_text = "🔥 **Топ Crypto Бонусів** 🔥\n\n"

    for b in bonuses:
        name = b.get('casino_name', 'Casino')
        offer = b.get('bonus_offer', 'N/A')
        wager = b.get('wagering', 'N/A')
        link = b.get('link', '#')  # Якщо лінку немає, ставимо заглушку

        # Робимо назву клікабельною через HTML тег <a>
        # <a href="посилання">Назва</a>
        message_text += f"🎰 <b><a href='{link}'>{name}</a></b>\n"
        message_text += f"💰 {offer}\n"
        message_text += f"🔄 {wager}\n"
        message_text += "-------------------\n"

    try:
        # Важливо: parse_mode='HTML' дозволяє робити посилання
        bot.send_message(CHAT_ID, message_text, parse_mode='HTML', disable_web_page_preview=True)
        print("✅ Відправлено!")
    except Exception as e:
        print(f"❌ Помилка Telegram: {e}")


if __name__ == "__main__":
    send_new_bonuses()