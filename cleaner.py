# Файл: src/cleaner.py
from bs4 import BeautifulSoup


def clean_html_content(raw_html: str) -> str:
    """
    Приймає брудний HTML, викидає рекламу, скрипти, стилі,
    і повертає чисту структуру для AI.
    """
    if not raw_html:
        return ""

    soup = BeautifulSoup(raw_html, "html.parser")

    # 1. Видаляємо сміттєві теги (скрипти, стилі, футери, навігацію)
    useless_tags = [
        "script", "style", "svg", "noscript",
        "header", "footer", "nav", "iframe", "meta", "link"
    ]
    for tag in soup(useless_tags):
        tag.decompose()  # Повністю видаляє тег з дерева

    # 2. Очищаємо HTML від класів та ID (вони займають купу місця, але AI вони не треба)
    # Наприклад: <div class="col-md-12 container-fluid wrapper"> -> <div>
    for tag in soup.find_all(True):
        tag.attrs = {}  # Видаляємо всі атрибути

    # 3. Повертаємо тільки тіло сторінки (без <head>)
    if soup.body:
        return str(soup.body)

    return str(soup)