# Файл: src/dynamic_data.py (Виправлений з екрануванням Markdown)
import requests
from bs4 import BeautifulSoup
import textwrap


def escape_markdown(text):
    """
    Екранує спеціальні символи, які можуть порушити Markdown-розбір Telegram.
    Це застосовується до тексту, отриманого з зовнішніх джерел (парсингу).
    """
    # Символи, які Telegram інтерпретує як Markdown V1 (за замовчуванням)
    special_chars = ['_', '*', '`', '[', ']', '(', ')']

    # Екрануємо зворотною скісною рискою
    for char in special_chars:
        text = text.replace(char, f'\\{char}')

    # Окремо екрануємо символ \ (подвійне екранування)
    text = text.replace('\\', '\\\\')

    return text


def get_dynamic_airdrops(limit=3):
    """
    Парсить сторінку AirdropAlert.com для отримання свіжих airdrops.
    """

    AIRDROP_URL = "https://airdropalert.com/new"
    airdrops = []

    print(f"📡 Парсимо динамічні Airdrops з {AIRDROP_URL}...")

    try:
        # Використовуємо User-Agent для імітації браузера
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(AIRDROP_URL, headers=headers, timeout=10)
        response.raise_for_status()  # Викликає помилку для 4xx/5xx статусів

        soup = BeautifulSoup(response.text, 'html.parser')

        # Шукаємо елементи, які містять список airdrops
        items = soup.select('div.card.airdrop-card')

        for item in items[:limit]:
            title_tag = item.select_one('h2.card-title a')
            desc_tag = item.select_one('p.card-text')

            if title_tag and title_tag.get('href'):
                title = title_tag.text.strip()
                link = AIRDROP_URL + title_tag['href'] if title_tag['href'].startswith('/') else title_tag['href']

                description = desc_tag.text.strip() if desc_tag else "Деталі на сайті."
                short_desc = textwrap.shorten(description, width=80, placeholder="...")

                # --- КРОК ВИПРАВЛЕННЯ: ЕКРАНУВАННЯ MARKDOWN ---
                # Це запобігає помилкам "can't parse entities"
                title = escape_markdown(title)
                short_desc = escape_markdown(short_desc)
                # ---------------------------------------------

                airdrops.append({
                    "source": "AirdropAlert (Парсинг)",
                    "title": title,
                    "link": link,
                    "description": short_desc
                })

        return airdrops

    except requests.exceptions.RequestException as e:
        print(f"❌ Помилка з'єднання/парсингу Airdrops: {e}")
        return []
    except Exception as e:
        print(f"❌ Невідома помилка парсингу: {e}")
        return []


if __name__ == '__main__':
    print(get_dynamic_airdrops())