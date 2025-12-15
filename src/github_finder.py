# Файл: src/github_finder.py
import requests
import textwrap

# Важливо: Для великих обсягів пошуку потрібен GitHub Token
# Ми використовуємо Public API для простого пошуку (ліміт: 10 запитів/хвилину)
GITHUB_SEARCH_URL = "https://api.github.com/search/issues"

# Приклад популярних репозиторіїв, де публікують вакансії (Issues)
# Ми шукаємо issues з тегом 'job', 'hiring' або 'vacancy'
QUERY = 'label:job,hiring,vacancy type:issue state:open'


def get_github_jobs(limit=5):
    """
    Шукає актуальні вакансії на GitHub у Issues за спеціальними тегами.
    """
    print(f"🔗 Шукаю відкриті Issues (вакансії) на GitHub...")

    params = {
        'q': QUERY,
        'sort': 'updated',
        'order': 'desc',
        'per_page': limit
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json',
        # Якщо матимете TOKEN, додайте: 'Authorization': f'token {YOUR_GITHUB_TOKEN}'
    }

    try:
        response = requests.get(GITHUB_SEARCH_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        jobs_list = []

        for item in data.get('items', []):
            # Чистимо опис (беремо початок тіла Issue)
            body = item.get('body', 'Опис відсутній. Див. посилання.')
            clean_desc = body.replace('\n', ' ').replace('*', '').replace('__', '')
            short_desc = textwrap.shorten(clean_desc, width=150, placeholder="...")

            jobs_list.append({
                "source": f"GitHub Issues ({item['repository_url'].split('/')[-1]})",
                "title": item['title'],
                "link": item['html_url'],
                "description": short_desc
            })

        if not jobs_list:
            # Якщо немає результатів, повертаємо заглушку
            return [{
                "source": "GitHub",
                "title": "Вакансії не знайдено за поточним запитом",
                "link": "https://github.com/search?type=Issues&q=label%3Ahiring",
                "description": "Спробуйте змінити ключові слова або перевірте GitHub напряму."
            }]

        return jobs_list

    except requests.exceptions.RequestException as e:
        print(f"❌ Помилка GitHub API: {e}")
        return f"Помилка підключення до GitHub API: {e}"


if __name__ == '__main__':
    jobs = get_github_jobs(3)
    for job in jobs:
        print(f"[{job['title']}]({job['link']})")