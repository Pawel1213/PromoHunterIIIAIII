# Файл: src/chat_bot.py (ВИПРАВЛЕНО: ЗАПУСК ТА ВІДСТУПИ)
import os
import telebot
from telebot import types
import google.generativeai as genai
from dotenv import load_dotenv
from supabase import create_client, Client
import datetime
from datetime import timezone
import re

# --- УТИЛІТИ ---
def clean_markdown_v1(text):
    """Екранує символи для Markdown V1."""
    if not isinstance(text, str):
        return text
    special_chars = ['_', '*', '`', '[', ']', '(', ')']
    for char in special_chars:
        text = text.replace(char, '\\' + char)
    return text


# --- ІМПОРТИ ---
try:
    from src.freelance import get_open_jobs
except ImportError:
    from src.freelance import get_open_jobs

try:
    from info_center import get_microtask_summary, get_earning_opportunities
except ImportError:
    from info_center import get_microtask_summary, get_earning_opportunities

try:
    from github_finder import get_github_jobs
except ImportError:
    from github_finder import get_github_jobs

# НОВИЙ ІМПОРТ: REDDIT
try:
    from reddit_finder import get_reddit_freebies
except ImportError:
    from reddit_finder import get_reddit_freebies

# 1. Налаштування
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

print("🧠 AI-Bot (Fixed V1.2) готовий! (Ctrl+C щоб зупинити)")


# --- МЕНЮ (11 КНОПОК) ---
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🔥 Топ Бонусів")
    btn2 = types.KeyboardButton("🎰 Бездепозитні")
    btn3 = types.KeyboardButton("💰 Актуальний заробіток")
    btn4 = types.KeyboardButton("💻 Вакансії (Telegram)")
    btn5 = types.KeyboardButton("📊 Центр мікрозадач")
    btn6 = types.KeyboardButton("🐙 GitHub Вакансії")
    btn7 = types.KeyboardButton("🔎 Фільтр Вакансій")
    btn8 = types.KeyboardButton("⏳ Свіжі Акції (24h)")
    btn9 = types.KeyboardButton("⭐ Моє Улюблене")
    btn10 = types.KeyboardButton("🛡 Перевірка на СКАМ")
    btn11 = types.KeyboardButton("🎁 Халява (Reddit)")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
    return markup


# --- КНОПКА ЗБЕРЕЖЕННЯ ---
def create_save_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="⭐️ Зберегти в Улюблене", callback_data="save_this_item"))
    return markup


# --- ОБРОБНИК ЗБЕРЕЖЕННЯ ---
@bot.callback_query_handler(func=lambda call: call.data == "save_this_item")
def callback_save_item(call):
    try:
        user_id = call.from_user.id
        message = call.message

        extracted_link = None
        extracted_title = "Збережений елемент"

        # 1. Пошук посилання
        if message.entities:
            for entity in message.entities:
                if entity.type == "text_link":
                    extracted_link = entity.url
                    break
                elif entity.type == "url":
                    extracted_link = message.text[entity.offset: entity.offset + entity.length]
                    break

        if not extracted_link:
            url_match = re.search(r'(https?://[^\s]+)', message.text)
            if url_match:
                extracted_link = url_match.group(0).rstrip(')')

        if not extracted_link:
            bot.answer_callback_query(call.id, "❌ Не знайдено посилання.")
            return

        # 2. Пошук заголовка
        lines = message.text.split('\n')
        for line in lines:
            # Шукаємо рядки з нашими іконками
            if any(icon in line for icon in ["💼", "🔗", "🔥", "ℹ️", "🎁"]):
                clean_line = line
                for char in ["💼", "🔗", "🔥", "ℹ️", "🎁", "**"]:
                    clean_line = clean_line.replace(char, "")
                extracted_title = clean_line.split('](')[0].replace('[', '').strip()
                break

        # 3. Перевірка дублікатів
        existing = supabase.table("saved_items").select("*").eq("user_id", user_id).eq("link", extracted_link).execute()

        if existing.data:
            bot.answer_callback_query(call.id, "⚠️ Вже збережено!")
        else:
            supabase.table("saved_items").insert({
                "user_id": user_id,
                "title": extracted_title,
                "link": extracted_link,
                "source": "Bot Save"
            }).execute()

            bot.answer_callback_query(call.id, "✅ Збережено!")
            bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=None)

    except Exception as e:
        print(f"Save error: {e}")
        bot.answer_callback_query(call.id, "❌ Помилка БД.")


# --- ПРИВІТАННЯ ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Обирай опцію 👇", reply_markup=create_main_menu())


# --- ОБРОБНИК ФІЛЬТРАЦІЇ ---
def process_filter_step(message):
    chat_id = message.chat.id
    raw_keyword = message.text.strip()
    keywords = [kw.strip() for kw in raw_keyword.replace('/', ',').replace(',', ' ').split() if kw.strip()]

    if not keywords:
        bot.send_message(chat_id, "❌ Введіть хоча б одне слово.", reply_markup=create_main_menu())
        return

    keyword_display = ", ".join(keywords)
    bot.send_message(chat_id, f"🔍 Фільтрую Telegram-вакансії: **{keyword_display}**...", parse_mode='Markdown')

    try:
        jobs = get_open_jobs(limit=5, keyword=keywords)
        if isinstance(jobs, str) or not jobs:
            bot.send_message(chat_id, f"😔 Нічого не знайдено для '{keyword_display}'.")
        else:
            bot.send_message(chat_id, f"💡 **Результати пошуку ({keyword_display}):**", parse_mode='Markdown')
            for job in jobs:
                source = clean_markdown_v1(job['source'])
                title = clean_markdown_v1(job['title'])
                desc = clean_markdown_v1(job['description'])

                text = f"ℹ️ **{source}**\n💼 [{title}]({job['link']})\n📝 _{desc}_"
                bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_save_markup())

    except Exception as e:
        bot.send_message(chat_id, f"❌ Помилка: {e}")

    bot.send_message(chat_id, "Обери дію:", reply_markup=create_main_menu())


# --- ОБРОБНИК SCAM CHECKER ---
def process_scam_check_step(message):
    chat_id = message.chat.id
    link = message.text.strip()

    if "." not in link:
        bot.send_message(chat_id, "⚠️ Це не схоже на посилання.", reply_markup=create_main_menu())
        return

    bot.send_chat_action(chat_id, 'typing')
    bot.send_message(chat_id, f"🛡 Аналізую ресурс: {link} ...")

    try:
        prompt = f"""
        Ти - експерт з кібербезпеки.
        Аналізуй посилання: "{link}"
        1. Назва домену (бренд чи клон?).
        2. Відомі схеми скаму.
        3. Ризик: НИЗЬКИЙ/СЕРЕДНІЙ/ВИСОКИЙ.
        4. Висновок українською.
        """
        response = model.generate_content(prompt)
        bot.send_message(chat_id, response.text, parse_mode='Markdown')

    except Exception as e:
        bot.send_message(chat_id, f"❌ Помилка аналізу: {e}")

    bot.send_message(chat_id, "Обери наступну дію:", reply_markup=create_main_menu())


# --- ГОЛОВНА ЛОГІКА ---
@bot.message_handler(func=lambda message: True)
def handle_query(message):
    user_query = message.text.lower()
    chat_id = message.chat.id
    print(f"👤 Запит: {user_query}")

    # === БЛОК 1: АКТУАЛЬНИЙ ЗАРОБІТОК ===
    if "заробіток" in user_query and "актуальний" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        try:
            opportunities = get_earning_opportunities()
            response_text = "💰 **АКТУАЛЬНИЙ ЗАРОБІТОК**\n\n"
            for item in opportunities:
                if item['link'] == "#":
                    title = clean_markdown_v1(item['title'].strip('*_'))
                    response_text += f"\n---\n**{title}**\n"
                else:
                    source = clean_markdown_v1(item['source'])
                    title = clean_markdown_v1(item['title'].replace("🔗 ", ""))
                    response_text += f"*{source}*\n🔗 [{title}]({item['link']})\n-------------------\n"
            bot.reply_to(message, response_text, parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, f"❌ Помилка: {e}")
        return

    # === БЛОК 2: МІКРОЗАДАЧІ ===
    if "мікрозадач" in user_query or "центр" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        try:
            summary = get_microtask_summary()
            response_text = "✨ **Огляд платформ:**\n\n"
            for item in summary:
                title = clean_markdown_v1(item['title'])
                response_text += f"ℹ️ **{item['source']}**\n🔗 [{title}]({item['link']})\n---\n"
            bot.reply_to(message, response_text, parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, f"❌ Помилка: {e}")
        return

    # === БЛОК 3: ВАКАНСІЇ TELEGRAM ===
    if "вакансії" in user_query and "telegram" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        bot.reply_to(message, "🔍 Шукаю вакансії у Telegram (Online)...")
        try:
            jobs = get_open_jobs(limit=5)
            if isinstance(jobs, str) or not jobs:
                bot.reply_to(message, "😔 Вакансій наразі не знайдено.")
            else:
                for job in jobs:
                    source = clean_markdown_v1(job['source'])
                    title = clean_markdown_v1(job['title'])
                    desc = clean_markdown_v1(job['description'])

                    text = f"ℹ️ **{source}**\n💼 [{title}]({job['link']})\n📝 _{desc}_"
                    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_save_markup())
        except Exception as e:
            bot.reply_to(message, f"❌ Помилка Telethon: {e}")
        return

    # === БЛОК 4: ВАКАНСІЇ GITHUB ===
    if "github" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        bot.reply_to(message, "🔍 Шукаю вакансії на GitHub...")
        try:
            jobs = get_github_jobs(limit=5)
            if isinstance(jobs, str):
                bot.reply_to(message, jobs)
            else:
                for job in jobs:
                    source = clean_markdown_v1(job['source'])
                    title = clean_markdown_v1(job['title'])
                    desc = clean_markdown_v1(job['description'])

                    text = f"ℹ️ **{source}**\n💼 [{title}]({job['link']})\n📝 _{desc}_"
                    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_save_markup())
        except Exception as e:
            bot.reply_to(message, f"❌ Помилка: {e}")
        return

    # === БЛОК 10: ХАЛЯВА REDDIT (ВИПРАВЛЕНО ВІДСТУПИ) ===
    if "халява" in user_query or "reddit" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        bot.reply_to(message, "🎁 Перевіряю Reddit (r/freebies, r/giveaways)...")
        try:
            freebies = get_reddit_freebies(limit=5)

            if isinstance(freebies, list) and len(freebies) > 0 and isinstance(freebies[0], str) and "⚠️" in freebies[0]:
                bot.reply_to(message, freebies[0])
                return

            if isinstance(freebies, str):
                bot.reply_to(message, freebies)
            else:
                for item in freebies:
                    text = f"🎁 {item['source']}\n"
                    text += f"{item['title']}\n"
                    text += f"🔗 {item['link']}\n"
                    text += f"📝 {item['description']}"
                    bot.send_message(chat_id, text, reply_markup=create_save_markup())
        except Exception as e:
            bot.reply_to(message, f"❌ Помилка обробки Reddit: {e}")
        return

    # === БЛОК 5: ФІЛЬТР ВАКАНСІЙ ===
    if "фільтр вакансій" in user_query:
        msg = bot.reply_to(message, "Введіть ключові слова:")
        bot.register_next_step_handler(msg, process_filter_step)
        return

    # === БЛОК 6: СВІЖІ АКЦІЇ (24H) ===
    if "свіжі акції" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        bot.reply_to(message, "⏳ Шукаю за останні 24 години...")

        response_text = "✨ **НОВИНКИ (24h):**\n\n"
        try:
            jobs = get_open_jobs(limit=3)
            if jobs and isinstance(jobs, list):
                response_text += "**💻 Telegram:**\n"
                for job in jobs:
                    response_text += f"- [{clean_markdown_v1(job['title'])}]({job['link']})\n"

            g_jobs = get_github_jobs(limit=2)
            if g_jobs and isinstance(g_jobs, list) and "не знайдено" not in g_jobs[0]['title']:
                response_text += "\n**🐙 GitHub:**\n"
                for job in g_jobs:
                    response_text += f"- [{clean_markdown_v1(job['title'])}]({job['link']})\n"

            if "Telegram" not in response_text and "GitHub" not in response_text:
                bot.reply_to(message, "😔 За останні 24 години нічого цікавого.")
            else:
                bot.reply_to(message, response_text, parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, f"Помилка: {e}")
        return

    # === БЛОК 8: МОЄ УЛЮБЛЕНЕ ===
    if "улюблене" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        try:
            response = supabase.table("saved_items").select("*").eq("user_id", chat_id).order("created_at",
                                                                                              desc=True).execute()
            items = response.data

            if not items:
                bot.reply_to(message, "📭 У вас поки немає збережених елементів.")
            else:
                text = "⭐️ **ВАШІ ЗБЕРЕЖЕНІ ЕЛЕМЕНТИ:**\n\n"
                for item in items:
                    title = clean_markdown_v1(item.get('title', 'Посилання'))
                    link = item.get('link', '#')
                    text += f"📌 [{title}]({link})\n"
                bot.reply_to(message, text, parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, f"❌ Помилка отримання збережених: {e}")
        return

    # === БЛОК 9: ПЕРЕВІРКА НА СКАМ ===
    if "скам" in user_query or "перевірка" in user_query:
        msg = bot.reply_to(message, "🔗 Надішліть посилання (URL):")
        bot.register_next_step_handler(msg, process_scam_check_step)
        return

    # === БЛОК 7: AI (DEFAULT) ===
    bot.send_chat_action(chat_id, 'typing')
    try:
        response = supabase.table("bonuses").select("*").order("created_at", desc=True).limit(20).execute()
        prompt = f"""
        База бонусів казино: {str(response.data)}
        Запит користувача: "{message.text}"
        Відповідай українською. Якщо питають про скам - порадь кнопку '🛡 Перевірка на СКАМ'.
        Якщо питають про халяву - порадь '🎁 Халява (Reddit)'.
        """
        ai_resp = model.generate_content(prompt)
        bot.reply_to(message, ai_resp.text, parse_mode='Markdown')
    except:
        bot.reply_to(message, "Я тут, але виникла помилка AI.")


if __name__ == "__main__":
    # ЗАПУСК ТУТ - ЦЕ ПРАВИЛЬНО
    bot.infinity_polling(timeout=60, long_polling_timeout=60)