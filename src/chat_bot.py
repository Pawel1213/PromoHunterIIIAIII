# Файл: src/chat_bot.py (ВЕРСИЯ 2.1: ФІКСড)
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
    get_open_jobs = None

try:
    from src.info_center import get_microtask_summary, get_earning_opportunities
except ImportError:
    get_earning_opportunities = None

try:
    from src.github_finder import get_github_jobs
except ImportError:
    get_github_jobs = None

try:
    from src.reddit_finder import get_reddit_freebies
except ImportError:
    get_reddit_freebies = None

# === НОВЫЙ ИМПОРТ: РАСШИРЕННЫЙ ПАРСЕР (49 ИСТОЧНИКОВ) ===
try:
    from src.parsers import get_all_opportunities, get_opportunities_by_category
    print("✅ parsers.py успешно импортирован (49 источников)")
except ImportError:
    try:
        from parsers import get_all_opportunities, get_opportunities_by_category
        print("✅ parsers.py успешно импортирован (локально)")
    except ImportError:
        print("❌ ОШИБКА: parsers.py не найден!")
        get_opportunities_by_category = None
        get_all_opportunities = None

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

print("✅ PromoHunter Bot v2.1 готов к запуску!")


# --- ГЛАВНОЕ МЕНЮ ---
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn1 = types.KeyboardButton("🌍 КАТАЛОГ (49 ист.)")
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
    markup.add(types.InlineKeyboardButton(text="⭐️ Зберегти", callback_data="save_this_item"))
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
            extracted_title = lines[0].replace("🔗", "").replace("👉", "").replace("⚠️", "").strip()[:100]

        existing = supabase.table("saved_items").select("*").eq("user_id", user_id).eq("link", extracted_link).execute()

        if existing.data:
            bot.answer_callback_query(call.id, "⚠️ Вже збережено!")
        else:
            supabase.table("saved_items").insert({
                "user_id": user_id,
                "title": extracted_title,
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
    bot.reply_to(message, "Привіт! 👋 Обирай категорію 👇", reply_markup=create_main_menu())


# --- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ОТПРАВКИ СПИСКА ---
def send_catalog_category(chat_id, category_key, category_name):
    """Отправить список источников по категории"""
    
    if get_opportunities_by_category is None:
        bot.send_message(chat_id, "❌ Модуль каталогу не підключено (parsers.py не знайдено).")
        return

    try:
        items = get_opportunities_by_category(category_key)
    except Exception as e:
        bot.send_message(chat_id, f"❌ Помилка при отримані даних: {str(e)}")
        print(f"Error fetching category {category_key}: {e}")
        return

    if not items or len(items) == 0:
        bot.send_message(chat_id, f"📭 У категорії '{category_name}' поки пусто.")
        return

    # Заголовок
    header = f"📂 **{category_name}** ({len(items)} джерел)\n\n"
    bot.send_message(chat_id, header, parse_mode='Markdown')

    # Відправляємо кожен item
    for i, item in enumerate(items, 1):
        try:
            title = clean_markdown_v1(item.get('title', 'No title'))
            description = clean_markdown_v1(item.get('description', 'No description'))
            link = item.get('link', '#')
            emoji = item.get('emoji', '🔹')
            legality = item.get('legality', 'Legal')

            # Формуємо текст
            warning = ""
            if legality == 'Black':
                warning = "\n\n🛑 **УВАГА:** Цей ресурс НЕЛЕГАЛЬНИЙ! Використовуйте тільки для ознайомлення."
            elif legality == 'Grey':
                warning = "\n⚠️ _Обережно: Сіра зона._"

            text = f"{emoji} **[{title}]({link})**\n\n_{description}_{warning}"

            # Відправляємо з кнопкою
            bot.send_message(
                chat_id,
                text,
                parse_mode='Markdown',
                disable_web_page_preview=True,
                reply_markup=create_save_markup()
            )

            # Затримка щоб Telegram не вдарив по rate limit
            import time
            if i % 5 == 0:
                time.sleep(1)

        except Exception as e:
            print(f"Error sending item {i}: {e}")
            continue


# --- ГЛАВНЫЙ ОБРАБОТЧИК ---
@bot.message_handler(func=lambda message: True)
def handle_query(message):
    user_query = message.text.lower()
    chat_id = message.chat.id

    # === НАВИГАЦІЯ КАТАЛОГУ ===
    if message.text == "🌍 КАТАЛОГ (49 ист.)":
        bot.send_message(chat_id, "Оберіть розділ каталогу:", reply_markup=create_catalog_menu())
        return

    if message.text == "🔙 Назад в меню":
        bot.send_message(chat_id, "Головне меню:", reply_markup=create_main_menu())
        return

    # Обработка кнопок подменю (Маппинг на ключи из parsers.py)
    if "заробіток" in user_query:
        send_catalog_category(chat_id, "earnings", "💰 Заробіток")
        return
    if "бонуси" in user_query:
        send_catalog_category(chat_id, "bonuses", "🎰 Бонуси")
        return
    if "скрипти" in user_query:
        send_catalog_category(chat_id, "scripts", "🛠 Скрипти та Інструменти")
        return
    if "пропозиції" in user_query:
        send_catalog_category(chat_id, "proposals", "💡 Нові Пропозиції")
        return
    if "сірі ніші (снд)" in user_query or ("сірі" in user_query and "снд" in user_query):
        bot.send_message(
            chat_id,
            "⚠️ **Вхід у зону підвищеного ризику!**\n\nЦя інформація надається виключно в освітніх цілях. Використання цих ресурсів може бути незаконним у вашій країні.",
            parse_mode='Markdown'
        )
        send_catalog_category(chat_id, "grey_niche_cis", "🕷️ Сірі Ніші (СНД)")
        return
    if "сірі ніші (європа)" in user_query or ("сірі" in user_query and "європа" in user_query):
        bot.send_message(chat_id, "⚠️ **Вхід у зону підвищеного ризику!**", parse_mode='Markdown')
        send_catalog_category(chat_id, "grey_niche_europe", "🇪🇺 Сірі Ніші (Європа)")
        return
    if "сірі ніші (сша)" in user_query or ("сірі" in user_query and "сша" in user_query):
        bot.send_message(chat_id, "⚠️ **Вхід у зону підвищеного ризику!**", parse_mode='Markdown')
        send_catalog_category(chat_id, "grey_niche_usa", "🇺🇸 Сірі Ніші (США)")
        return
    if "легальні" in user_query and "маркет" in user_query:
        send_catalog_category(chat_id, "legal_marketplaces", "⚖️ Легальні Маркетплейси")
        return

    # === СТАРЫЕ ФУНКЦИИ ===

    # 1. POZNAN GIGS
    if "познань" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        poznan_items = get_opportunities_by_category("poznan_gigs")
        if poznan_items:
            response_text = "🇵🇱 **ПІДРОБІТОК ПОЗНАНЬ:** (9 джерел)\n\n"
            for gig in poznan_items:
                title = clean_markdown_v1(gig['title'])
                link = gig['link']
                emoji = gig.get('emoji', '👉')
                rate = gig.get('min_earning', 0)
                response_text += f"{emoji} [{title}]({link})\n💰 {rate} zł/h\n\n"
            bot.send_message(chat_id, response_text, parse_mode='Markdown', disable_web_page_preview=True)
        else:
            bot.reply_to(message, "❌ Дані про Познань не знайдені.")
        return

    # 2. TELEGRAM JOBS
    if "вакансії" in user_query and "telegram" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        if get_open_jobs:
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
        else:
            bot.reply_to(message, "❌ Модуль не доступний.")
        return

    # 3. GITHUB
    if "github" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        if get_github_jobs:
            try:
                jobs = get_github_jobs(limit=5)
                if isinstance(jobs, list):
                    for job in jobs:
                        text = f"🐙 [{clean_markdown_v1(job['title'])}]({job['link']})\n📝 {clean_markdown_v1(job['description'])}"
                        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_save_markup())
                else:
                    bot.reply_to(message, str(jobs))
            except Exception as e:
                bot.reply_to(message, f"Error: {e}")
        else:
            bot.reply_to(message, "❌ GitHub модуль не знайден.")
        return

    # 4. REDDIT FREEBIES
    if "халява" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        if get_reddit_freebies:
            try:
                freebies = get_reddit_freebies(limit=5)
                if isinstance(freebies, list) and len(freebies) > 0:
                    for item in freebies:
                        text = f"🎁 {item['title']}\n🔗 {item['link']}"
                        bot.send_message(chat_id, text, reply_markup=create_save_markup())
                else:
                    bot.reply_to(message, str(freebies) if freebies else "Нічого не знайдено.")
            except Exception as e:
                bot.reply_to(message, f"Error: {e}")
        else:
            bot.reply_to(message, "❌ Reddit модуль не знайден.")
        return

    # 5. ACTUAL EARNINGS
    if "актуальний" in user_query and "заробіток" in user_query:
        bot.send_chat_action(chat_id, 'typing')
        if get_earning_opportunities:
            try:
                opps = get_earning_opportunities()
                txt = "💰 **Актуальні можливості заробітку:**\n\n"
                for item in opps:
                    if item['link'] == "#":
                        txt += f"\n**{clean_markdown_v1(item['title'])}**\n"
                    else:
                        txt += f"🔗 [{clean_markdown_v1(item['title'])}]({item['link']})\n"
                bot.send_message(chat_id, txt, parse_mode='Markdown', disable_web_page_preview=True)
            except Exception as e:
                bot.reply_to(message, f"Error: {e}")
        else:
            bot.reply_to(message, "❌ Модуль не доступний.")
        return

    # 6. FAVORITES
    if "улюблене" in user_query or "улюбленое" in user_query:
        try:
            res = supabase.table("saved_items").select("*").eq("user_id", chat_id).order("created_at", desc=True).execute()
            if not res.data:
                bot.reply_to(message, "📭 Ви ще нічого не зберегли.")
            else:
                txt = "⭐️ **Ваше улюблене:**\n\n"
                for i in res.data:
                    title = clean_markdown_v1(i.get('title', 'Link'))
                    txt += f"📌 [{title}]({i['link']})\n"
                bot.send_message(chat_id, txt, parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e:
            print(f"Favorites error: {e}")
            bot.reply_to(message, "❌ Помилка при отриманні улюбленого.")
        return

    # 7. DEFAULT AI RESPONSE
    bot.send_chat_action(chat_id, 'typing')
    try:
        prompt = f"Користувач пише: '{message.text}'. Відповідай коротко українською мовою. Ти - бот PromoHunter який допомагає людям знаходити способи заробітку."
        resp = model.generate_content(prompt)
        bot.reply_to(message, resp.text[:4096], parse_mode='Markdown')  # Ліміт 4096 символів
    except Exception as e:
        print(f"AI error: {e}")
        bot.reply_to(message, "🤖 Я тут, але AI відпочиває. Спробуйте пізніше.")


if __name__ == "__main__":
    print("🚀 Запуск PromoHunter Bot v2.1...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)
