# Файл: src/chat_bot.py (ВЕРСИЯ 2.1: С ПОЗНАНЬЮ И РАСШИРЕННЫМ КАТАЛОГОМ)
import os
import telebot
from telebot import types
import google.generativeai as genai
from dotenv import load_dotenv
from supabase import create_client, Client
import re


# --- УТИЛИТЫ ---
def clean_markdown_v1(text):
    """Экранирует символы для Markdown V1."""
    if not isinstance(text, str):
        return str(text)
    special_chars = ['_', '*', '`', '[', ']', '(', ')']
    for char in special_chars:
        text = text.replace(char, '\\' + char)
    return text


# --- ИМПОРТЫ МОДУЛЕЙ ---
try:
    from src.freelance import get_open_jobs
except ImportError:
    from freelance import get_open_jobs

try:
    from src.info_center import get_microtask_summary, get_earning_opportunities
except ImportError:
    from info_center import get_microtask_summary, get_earning_opportunities

try:
    from src.github_finder import get_github_jobs
except ImportError:
    from github_finder import get_github_jobs

try:
    from src.reddit_finder import get_reddit_freebies
except ImportError:
    from reddit_finder import get_reddit_freebies

# POZNAN GIGS
try:
    from src.poznan_gigs import get_poznan_gigs
except ImportError:
    get_poznan_gigs = None

# --- НОВЫЙ ИМПОРТ: РАСШИРЕННЫЙ ПАРСЕР (49 ИСТОЧНИКОВ) ---
try:
    from src.PARSERS_EXPANDED import get_opportunities_by_category
except ImportError:
    try:
        from PARSERS_EXPANDED import get_opportunities_by_category
    except ImportError:
        print("⚠️ Файл PARSERS_EXPANDED.py не найден!")
        get_opportunities_by_category = None

# --- КОНФИГУРАЦИЯ ---
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

print("🧠 AI-Bot (Expanded v2.1) готов! (Ctrl+C для остановки)")


# --- ГЛАВНОЕ МЕНЮ ---
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn1 = types.KeyboardButton("🌍 КАТАЛОГ (49 ист.)")  # <--- НОВАЯ ГЛАВНАЯ КНОПКА
    btn2 = types.KeyboardButton("🇵🇱 Робота Познань")
    btn3 = types.KeyboardButton("💻 Вакансії (Telegram)")
    btn4 = types.KeyboardButton("🐙 GitHub Вакансії")
    btn5 = types.KeyboardButton("🎁 Халява (Reddit)")
    btn6 = types.KeyboardButton("💰 Актуальний заробіток")
    btn7 = types.KeyboardButton("🔎 Фільтр Вакансій")
    btn8 = types.KeyboardButton("🛡 Перевірка на СКАМ")
    btn9 = types.KeyboardButton("⭐ Моє Улюблене")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    return markup


# --- ПОДМЕНЮ КАТАЛОГА ---
def create_catalog_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # Категории соответствуют вашему PARSERS_EXPANDED.py
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


# --- КНОПКА СОХРАНЕНИЯ ---
def create_save_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="⭐️ Зберегти в Улюблене", callback_data="save_this_item"))
    return markup


# --- ОБРАБОТЧИК СОХРАНЕНИЯ ---
@bot.callback_query_handler(func=lambda call: call.data == "save_this_item")
def callback_save_item(call):
    try:
        user_id = call.from_user.id
        message = call.message
        extracted_link = None
        extracted_title = "Збережений елемент"

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

        lines = message.text.split('\n')
        if lines:
            extracted_title = lines[0].replace("🔗", "").replace("👉", "").replace("⚠️", "").strip()

        existing = supabase.table("saved_items").select("*").eq("user_id", user_id).eq("link", extracted_link).execute()

        if existing.data:
            bot.answer_callback_query(call.id, "⚠️ Вже збережено!")
        else:
            supabase.table("saved_items").insert({
                "user_id": user_id,
                "title": extracted_title[:100],
                "link": extracted_link,
                "source": "Catalog Bot"
            }).execute()
            bot.answer_callback_query(call.id, "✅ Збережено!")

    except Exception as e:
        print(f"Save error: {e}")
        bot.answer_callback_query(call.id, "❌ Помилка БД.")


# --- КОМАНДА START ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Обирай категорію 👇", reply_markup=create_main_menu())


# --- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ОТПРАВКИ СПИСКА ---
def send_catalog_category(chat_id, category_key, category_name):
    if get_opportunities_by_category is None:
        bot.send_message(chat_id, "❌ Модуль каталогу не підключено.")
        return

    items = get_opportunities_by_category(category_key)
    if not items:
        bot.send_message(chat_id, f"📭 У категорії '{category_name}' поки пусто.")
        return

    bot.send_message(chat_id, f"📂 **Категорія: {category_name}** ({len(items)} джерел):", parse_mode='Markdown')

    for item in items:
        title = clean_markdown_v1(item['title'])
        desc = clean_markdown_v1(item['description'])
        link = item['link']
        emoji = item.get('emoji', '🔹')

        # Добавляем предупреждение для серых/черных ниш
        warning = ""
        if item.get('legality') == 'Black':
            warning = "\n🛑 **УВАГА: ЦЕЙ РЕСУРС МОЖЕ БУТИ НЕЛЕГАЛЬНИМ!** Використовуйте тільки для ознайомлення."
        elif item.get('legality') == 'Grey':
            warning = "\n⚠️ _Обережно: Сіра зона._"

        text = f"{emoji} [{title}]({link})\nℹ️ {desc}{warning}"

        # Отправляем сообщение с кнопкой сохранения
        bot.send_message(chat_id, text, parse_mode='Markdown', disable_web_page_preview=True,
                         reply_markup=create_save_markup())


# --- ГЛАВНЫЙ ОБРАБОТЧИК ---
@bot.message_handler(func=lambda message: True)
def handle_query(message):
    user_query = message.text.lower()
    chat_id = message.chat.id

    # === НАВИГАЦИЯ ПО КАТАЛОГУ (НОВОЕ) ===
    if message.text == "🌍 КАТАЛОГ (49 ист.)":
        bot.send_message(chat_id, "Оберіть розділ каталогу:", reply_markup=create_catalog_menu())
        return

    if message.text == "🔙 Назад в меню":
        bot.send_message(chat_id, "Головне меню:", reply_markup=create_main_menu())
        return

    # Обработка кнопок подменю (Маппинг на ключи из PARSERS_EXPANDED.py)
    if "заробіток (earnings)" in user_query:
        send_catalog_category(chat_id, "earnings", "Заробіток")
        return
    if "бонуси (bonuses)" in user_query:
        send_catalog_category(chat_id, "bonuses", "Бонуси")
        return
    if "скрипти (scripts)" in user_query:
        send_catalog_category(chat_id, "scripts", "Скрипти та Інструменти")
        return
    if "пропозиції (proposals)" in user_query:
        send_catalog_category(chat_id, "proposals", "Нові Пропозиції")
        return
    if "сірі ніші (снд)" in user_query:
        bot.send_message(chat_id,
                         "⚠️ **Вхід у зону підвищеного ризику!**\nІнформація надається виключно в освітніх цілях.",
                         parse_mode='Markdown')
        send_catalog_category(chat_id, "grey_niche_cis", "Сірі Ніші (СНД)")
        return
    if "сірі ніші (європа)" in user_query:
        bot.send_message(chat_id, "⚠️ **Вхід у зону підвищеного ризику!**", parse_mode='Markdown')
        send_catalog_category(chat_id, "grey_niche_europe", "Сірі Ніші (Європа)")
        return
    if "сірі ніші (сша)" in user_query:
        bot.send_message(chat_id, "⚠️ **Вхід у зону підвищеного ризику!**", parse_mode='Markdown')
        send_catalog_category(chat_id, "grey_niche_usa", "Сірі Ніші (США)")
        return
    if "легальні маркети" in user_query:
        send_catalog_category(chat_id, "legal_marketplaces", "Легальні Маркетплейси")
        return

    # === СТАРЫЕ ФУНКЦИИ ===

    # 1. POZNAN GIGS
    if "познань" in user_query:
        if get_poznan_gigs:
            bot.send_chat_action(chat_id, 'typing')
            gigs = get_poznan_gigs()
            response_text = "🇵🇱 **ПІДРОБІТОК ПОЗНАНЬ:**\n\n"
            for gig in gigs:
                title = clean_markdown_v1(gig['title'])
                link = gig['link']
                emoji = gig.get('emoji', '👉')
                rate = gig.get('min_earning', 0)
                response_text += f"{emoji} [{title}]({link})\n💰 {rate} zł/h\n---\n"
            bot.send_message(chat_id, response_text, parse_mode='Markdown', disable_web_page_preview=True)
        else:
            bot.reply_to(message, "❌ Модуль Познань не знайдено.")
        return

    # 2. TELEGRAM JOBS
    if "вакансії" in user_query and "telegram" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        bot.reply_to(message, "🔍 Шукаю вакансії у Telegram...")
        try:
            jobs = get_open_jobs(limit=5)
            if not jobs:
                bot.send_message(chat_id, "Вакансій не знайдено.")
            else:
                for job in jobs:
                    title = clean_markdown_v1(job['title'])
                    desc = clean_markdown_v1(job['description'])
                    text = f"ℹ️ {job['source']}\n💼 {title}\n📝 _{desc}_"
                    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_save_markup())
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
        return

    # 3. GITHUB
    if "github" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        jobs = get_github_jobs(limit=5)
        if isinstance(jobs, list):
            for job in jobs:
                text = f"🐙 [{clean_markdown_v1(job['title'])}]({job['link']})\n📝 {clean_markdown_v1(job['description'])}"
                bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_save_markup())
        else:
            bot.reply_to(message, str(jobs))
        return

    # 4. REDDIT FREEBIES
    if "халява" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        freebies = get_reddit_freebies(limit=5)
        if isinstance(freebies, list) and not isinstance(freebies[0], str):
            for item in freebies:
                text = f"🎁 {item['title']}\n🔗 {item['link']}"
                bot.send_message(chat_id, text, reply_markup=create_save_markup())
        else:
            bot.reply_to(message, str(freebies))
        return

    # 5. ACTUAL EARNINGS
    if "заробіток" in user_query and "актуальний" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        opps = get_earning_opportunities()
        txt = "💰 **Можливості:**\n\n"
        for item in opps:
            if item['link'] == "#":
                txt += f"\n**{clean_markdown_v1(item['title'])}**\n"
            else:
                txt += f"🔗 [{clean_markdown_v1(item['title'])}]({item['link']})\n"
        bot.send_message(chat_id, txt, parse_mode='Markdown', disable_web_page_preview=True)
        return

    # 6. SCAM CHECK
    if "скам" in user_query:
        bot.reply_to(message, "🔗 Надішліть посилання для перевірки.")
        # Тут можна додати register_next_step_handler, як у минулому коді
        return

    # 7. FAVORITES
    if "улюблене" in user_query:
        try:
            res = supabase.table("saved_items").select("*").eq("user_id", chat_id).order("created_at",
                                                                                         desc=True).execute()
            if not res.data:
                bot.reply_to(message, "📭 Пусто.")
            else:
                txt = "⭐️ **Збережене:**\n\n"
                for i in res.data:
                    txt += f"📌 [{clean_markdown_v1(i.get('title', 'Link'))}]({i['link']})\n"
                bot.send_message(chat_id, txt, parse_mode='Markdown', disable_web_page_preview=True)
        except:
            bot.reply_to(message, "Помилка БД.")
        return

    # 8. AI DEFAULT
    bot.send_chat_action(chat_id, 'typing')
    try:
        prompt = f"Користувач пише: {message.text}. Відповідай коротко українською. Ти бот PromoHunter."
        resp = model.generate_content(prompt)
        bot.reply_to(message, resp.text, parse_mode='Markdown')
    except:
        bot.reply_to(message, "Я тут, але AI відпочиває.")


if __name__ == "__main__":
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
