import os

# Шлях до файлу
path = os.path.join("src", "cleaner.py")

# Код, який буде всередині (наш "пилосос" для HTML)
code_content = """from bs4 import BeautifulSoup

def clean_html_content(raw_html: str) -> str:
    \"\"\"
    Приймає брудний HTML, викидає рекламу, скрипти, стилі,
    і повертає чисту структуру для AI.
    \"\"\"
    if not raw_html:
        return ""

    try:
        soup = BeautifulSoup(raw_html, "html.parser")

        # 1. Видаляємо сміттєві теги
        useless_tags = [
            "script", "style", "svg", "noscript", 
            "header", "footer", "nav", "iframe", "meta", "link"
        ]
        for tag in soup(useless_tags):
            tag.decompose()

        # 2. Очищаємо HTML від класів та атрибутів
        for tag in soup.find_all(True):
            tag.attrs = {}

        # 3. Повертаємо тіло або весь суп
        if soup.body:
            return str(soup.body)

        return str(soup)
    except Exception as e:
        print(f"⚠️ Помилка під час чистки HTML: {e}")
        return raw_html[:50000]  # Повертаємо як є, якщо BS4 впав
"""

print(f"🔨 Створюю файл {path}...")

try:
    with open(path, "w", encoding="utf-8") as f:
        f.write(code_content)
    print("✅ ГОТОВО! Файл cleaner.py успішно створено в папці src.")
except Exception as e:
    print(f"❌ Не вдалося створити файл: {e}")