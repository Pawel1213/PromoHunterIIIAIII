# Файл: src/cleaner.py
from bs4 import BeautifulSoup


def clean_html_content(raw_html: str) -> str:
    """
    Чистить HTML, але ЗАЛИШАЄ посилання (href) для AI.
    """
    if not raw_html:
        return ""

    try:
        soup = BeautifulSoup(raw_html, "html.parser")

        # 1. Видаляємо сміттєві теги
        useless_tags = [
            "script", "style", "svg", "noscript",
            "header", "footer", "nav", "iframe", "meta", "link", "form"
        ]
        for tag in soup(useless_tags):
            tag.decompose()

        # 2. Очищаємо атрибути, АЛЕ залишаємо href у посилань <a>
        for tag in soup.find_all(True):
            if tag.name == 'a' and tag.has_attr('href'):
                # Залишаємо тільки href, решту (класи, id) стираємо
                tag.attrs = {'href': tag['href']}
            else:
                tag.attrs = {}

        if soup.body:
            return str(soup.body)

        return str(soup)
    except Exception as e:
        print(f"⚠️ Помилка cleaner: {e}")
        return raw_html[:50000]