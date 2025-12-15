# Файл: src/engine.py
import asyncio
import json
import time
from src.ai.client import get_model
from src.hunters.web_scraper import WebHunter
from src.database import save_bonus
from src.cleaner import clean_html_content
from src.notifier import send_new_bonuses

# === СПИСОК ЦІЛЕЙ ===
TARGET_URLS = [
    "https://99bitcoins.com/bitcoin-casinos/",
    "https://www.analyticsinsight.net/cryptocurrency-analytics-news/best-crypto-casinos",
    "https://coinpedia.org/guest-post/best-crypto-casinos/",
    # Можете додавати сюди будь-які інші сайти з топами казино
]


async def run_bot_cycle():
    print(f"\n⏰ ЗАПУСК ЦИКЛУ ПОШУКУ ПО {len(TARGET_URLS)} САЙТАХ...")

    hunter = WebHunter(headless=True)
    model = get_model()

    # --- ГОЛОВНИЙ ЦИКЛ (Проходимо по кожному сайту) ---
    for url in TARGET_URLS:
        print(f"\n👉 [1/3] Обробляю сайт: {url}")

        try:
            # 1. Завантаження
            raw_html = await hunter.fetch_page_content(url)
            if not raw_html:
                print("⚠️ Пропускаю: не вдалося завантажити.")
                continue

            # 2. Чистка
            clean_html = clean_html_content(raw_html)
            print(f"   Розмір чистого коду: {len(clean_html)} символів")

            # 3. AI Аналіз
            print("   🧠 AI аналізує...")

            prompt = f"""
            Analyze this HTML code from a crypto news site.
            Task:
            1. Extract casino names, bonus offers, wagering, and LINKS (href).
            2. TRANSLATE 'bonus_offer' and 'wagering' to UKRAINIAN language.
            3. If link starts with /, append the domain {url} to it.

            Return JSON list:
            [
                {{
                    "casino_name": "Name",
                    "bonus_offer": "Ukrainian text",
                    "wagering": "Ukrainian text",
                    "link": "Full Link"
                }}
            ]

            HTML:
            {clean_html[:100000]} 
            """

            # Відправляємо запит до AI
            response = model.generate_content(prompt)

            # Обробка відповіді
            text_resp = response.text.replace("```json", "").replace("```", "").strip()
            if not text_resp.startswith("["):
                # Іноді AI пише вступ, шукаємо початок JSON
                start = text_resp.find("[")
                end = text_resp.rfind("]") + 1
                if start != -1 and end != -1:
                    text_resp = text_resp[start:end]

            bonuses = json.loads(text_resp)
            print(f"   🎉 Знайдено бонусів: {len(bonuses)}")

            # 4. Збереження
            for b in bonuses:
                # Виправляємо відносні посилання
                link = b.get("link", "")
                if link and link.startswith("/"):
                    # Якщо посилання відносне (/bonus), ліпимо до нього домен сайту
                    from urllib.parse import urlparse
                    parsed_uri = urlparse(url)
                    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                    link = domain + link

                save_bonus(
                    casino_name=b.get("casino_name", "Unknown"),
                    bonus_offer=b.get("bonus_offer", "No offer"),
                    wagering=b.get("wagering", "N/A"),
                    link=link
                )

            print("   ✅ Сайт оброблено успішно.")

        except Exception as e:
            print(f"   ❌ Помилка на цьому сайті: {e}")

        # ВАЖЛИВО: Пауза між сайтами, щоб не отримати бан від Google AI (Error 429)
        print("☕ Пауза 30 секунд перед наступним сайтом...")
        time.sleep(30)

    # --- КІНЕЦЬ ЦИКЛУ ---

    print("\n📲 Викликаю Telegram-бота...")
    send_new_bonuses()
    print("💤 Весь список пройдено. Чекаю наступного запуску за розкладом.")


if __name__ == "__main__":
    asyncio.run(run_bot_cycle())