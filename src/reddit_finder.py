# Файл: src/reddit_finder.py (ВИПРАВЛЕНО USER-AGENT)
import requests
from bs4 import BeautifulSoup
import textwrap
import random


def get_reddit_freebies(limit=5):
    """
    Парсить RSS-стрічки Reddit, маскуючись під звичайний браузер.
    """
    rss_url = "https://www.reddit.com/r/freebies+giveaways+GameDeals+steam_giveaway/new/.rss"

    # ВИКОРИСТОВУЄМО "СПРАВЖНІЙ" USER-AGENT (як у Chrome на Windows)
    # Це обходить захист Reddit, який відхиляє запити від скриптів
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # timeout=10 секунд, щоб не висіло вічно
        response = requests.get(rss_url, headers=headers, timeout=5)

        if response.status_code == 429:
            return ["⚠️ Забагато запитів до Reddit. Спробуйте через хвилину."]

        if response.status_code != 200:
            return [f"⚠️ Reddit відповів кодом {response.status_code}."]

        # Парсимо XML
        soup = BeautifulSoup(response.content, 'xml')
        entries = soup.find_all('entry')

        if not entries:
            return ["📭 Не вдалося розпарсити стрічку Reddit. Можливо, змінився формат."]

        results = []

        for entry in entries:
            try:
                title = entry.title.text
                link = entry.link['href']

                # Спроба дістати категорію
                category = "Reddit"
                if entry.category and 'term' in entry.category.attrs:
                    category = entry.category['term']
                elif entry.author and entry.author.find('name'):
                    category = entry.author.find('name').text.replace('/u/', '')

                # Опис
                content = entry.content.text if entry.content else ""
                clean_desc = BeautifulSoup(content, "html.parser").get_text()
                short_desc = textwrap.shorten(clean_desc, width=150, placeholder="...")

                results.append({
                    "source": f"r/{category}",
                    "title": title,
                    "link": link,
                    "description": short_desc
                })

                if len(results) >= limit:
                    break
            except Exception as parse_error:
                continue  # Пропускаємо "битий" пост, йдемо далі

        if not results:
            return "📭 На Reddit зараз тихо. Нових роздач не знайдено."

        return results

    except requests.exceptions.ConnectTimeout:
        return ["⚠️ Час очікування Reddit вичерпався (Timeout). Спробуйте пізніше."]
    except requests.exceptions.ConnectionError:
        return ["⚠️ Помилка з'єднання з Reddit. Перевірте інтернет."]
    except Exception as e:
        print(f"Global Reddit Error: {e}")
        return [f"❌ Помилка: {str(e)[:50]}"]


# Тест
if __name__ == "__main__":
    print("🔍 Тестування Reddit RSS...")
    items = get_reddit_freebies(5)
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict):
                print(f"- [{item['source']}] {item['title']}")
            else:
                print(item)
    else:
        print(items)