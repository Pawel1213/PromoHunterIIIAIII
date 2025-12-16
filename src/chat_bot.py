# Файл: src/chat_bot.py (FIXED IMPORT)
import os
import telebot
from telebot import types
import google.generativeai as genai
from dotenv import load_dotenv
from supabase import create_client, Client
import re
import time

# --- УТИЛІТИ ---
def clean_markdown_v1(text):
    """Екранує символи для Markdown V1."""
    if not isinstance(text, str):
        return str(text)
    special_chars = ['_', '*', '`', '[', ']', '(', ')']
    for char in special_chars:
        text = text.replace(char, '\\' + char)
    return text

# --- ІМПОРТИ МОДУЛІВ (ЗАХИЩЕНІ) ---
def safe_import(module_name, function_name):
    try:
        # Спроба 1: Імпорт як з пакету src (для серверу)
        mod = __import__(f"src.{module_name}", fromlist=[function_name])
        return getattr(mod, function_name)
    except ImportError:
        try:
            # Спроба 2: Локальний імпорт (для тестів)
            mod = __import__(module_name, fromlist=[function_name])
            return getattr(mod, function_name)
        except ImportError as e:
            print(f"⚠️ Модуль {module_name} не знайдено: {e}")
            return None

# Підключаємо функції
get_open_jobs = safe_import("freelance", "get_open_jobs")
get_microtask_summary = safe_import("info_center", "get_microtask_summary")
get_earning_opportunities = safe_import("info_center", "get_earning_opportunities")
get_github_jobs = safe_import("github_finder", "get_github_jobs")
get_reddit_freebies = safe_import("reddit_finder", "get_reddit_freebies")
get_poznan_gigs = safe_import("poznan_gigs", "get_poznan_gigs")

# ВАЖЛИВО: Імпорт розширеного каталогу
get_opportunities_by_category = safe_import("PARSERS_EXPANDED", "get_opportunities_by_category")

if get_opportunities_by_category is None:
    print("❌ КРИТИЧНО: PARSERS_EXPANDED.py не підключено! Перевірте файл у папці src.")

# --- КОНФІГУРАЦІЯ ---
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Налаштування AI (Google змінив бібліотеку, але старий метод ще працює з попередженням)
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    print(f"AI Config Error: {e}")
    model = None

print("🧠 AI-Bot (v2.2 Fixed) готовий!")

# --- МЕНЮ ---
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🌍 КАТАЛОГ (58 іст.)") # Оновлено кількість
    btn2 = types.KeyboardButton("🇵🇱 Робота Познань")
    btn3 = types.KeyboardButton("💻 Вакансії (Telegram)")
    btn4 = types.KeyboardButton("🎁 Халява (Reddit)")
    btn5 = types.KeyboardButton("💰 Актуальний заробіток")
    btn6 = types.KeyboardButton("⭐ Моє Улюблене")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

def create_catalog_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # Ключі повинні співпадати з PARSERS_EXPANDED.py
    btn1 = types.KeyboardButton("📂 Заробіток (Earnings)")
    btn2 = types.KeyboardButton("🎰 Бонуси (Bonuses)")
    btn3 = types.KeyboardButton("🛠 Скрипти (Scripts)")
    btn4 = types.KeyboardButton("💡 Пропозиції (Proposals)")
    btn5 = types.KeyboardButton("👽 Сірі Ніші (СНД)")
    btn6 = types.KeyboardButton("🇪🇺 Сірі Ніші (Європа)")
    btn7 = types.KeyboardButton("🇺🇸 Сірі Ніші (США)")
    btn8 = types.KeyboardButton("⚖️ Легальні Маркети")
    btn_back = types.KeyboardButton("🔙 Назад в меню")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn_back)
    return markup

# --- ФУНКЦІЇ ---
def send_catalog_category(chat_id, category_key, category_name):
    if get_opportunities_by_category is None:
        bot.send_message(chat_id, "❌ Помилка: Каталог не знайдено (файл відсутній).")
        return

    items = get_opportunities_by_category(category_key)
    if not items:
        bot.send_message(chat_id, f"📭 У категорії '{category_name}' пусто.")
        return

    bot.send_message(chat_id, f"📂 **{category_name}** ({len(items)}):", parse_mode='Markdown')
    
    for item in items:
        title = clean_markdown_v1(item['title'])
        desc = clean_markdown_v1(item['description'])
        link = item['link']
        emoji = item.get('emoji', '🔹')
        
        warning = ""
        if item.get('legality') == 'Black':
            warning = "\n🛑 **УВАГА: НЕЛЕГАЛЬНО! ТІЛЬКИ ДЛЯ ОЗНАЙОМЛЕННЯ!**"
        elif item.get('legality') == 'Grey':
            warning = "\n⚠️ _Сіра зона_"

        text = f"{emoji} [{title}]({link})\nℹ️ {desc}{warning}\n"
        bot.send_message(chat_id, text, parse_mode='Markdown', disable_web_page_preview=True)

# --- ОБРОБНИК ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привіт! Обирай категорію 👇", reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: True)
def handle_query(message):
    text = message.text.lower()
    chat_id = message.chat.id
    
    # Головне меню
    if message.text == "🌍 КАТАЛОГ (58 іст.)":
        bot.send_message(chat_id, "Оберіть розділ:", reply_markup=create_catalog_menu())
        return
    if message.text == "🔙 Назад в меню":
        bot.send_message(chat_id, "Меню:", reply_markup=create_main_menu())
        return

    # Каталог (Маппінг)
    if "заробіток (earnings)" in text: send_catalog_category(chat_id, "earnings", "Заробіток"); return
    if "бонуси (bonuses)" in text: send_catalog_category(chat_id, "bonuses", "Бонуси"); return
    if "скрипти (scripts)" in text: send_catalog_category(chat_id, "scripts", "Скрипти"); return
    if "пропозиції (proposals)" in text: send_catalog_category(chat_id, "proposals", "Пропозиції"); return
    if "сірі ніші (снд)" in text: send_catalog_category(chat_id, "grey_niche_cis", "СНД (Dark)"); return
    if "сірі ніші (європа)" in text: send_catalog_category(chat_id, "grey_niche_europe", "Європа (Dark)"); return
    if "сірі ніші (сша)" in text: send_catalog_category(chat_id, "grey_niche_usa", "США (Dark)"); return
    if "легальні маркети" in text: send_catalog_category(chat_id, "legal_marketplaces", "Маркетплейси"); return

    # Познань
    if "познань" in text and get_poznan_gigs:
        gigs = get_poznan_gigs()
        txt = "🇵🇱 **Познань:**\n\n"
        for g in gigs:
            txt += f"{g['emoji']} [{clean_markdown_v1(g['title'])}]({g['link']})\n💰 {g['min_earning']} zł/h\n\n"
        bot.send_message(chat_id, txt, parse_mode='Markdown', disable_web_page_preview=True)
        return

    # Reddit
    if "халява" in text and get_reddit_freebies:
        items = get_reddit_freebies(limit=5)
        if isinstance(items, list):
            for i in items:
                if isinstance(i, dict):
                    bot.send_message(chat_id, f"🎁 {i['title']}\n🔗 {i['link']}")
        return

    # AI Chat
    if model:
        try:
            resp = model.generate_content(f"Відповіж українською: {message.text}")
            bot.reply_to(message, resp.text, parse_mode='Markdown')
        except:
            bot.reply_to(message, "AI зараз недоступний.")
    else:
        bot.reply_to(message, "Я тут.")

# ЗАПУСК (ТІЛЬКИ ЯКЩО ФАЙЛ ЗАПУЩЕНО НАПРЯМУ)
if __name__ == "__main__":
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
