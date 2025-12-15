# Файл: test_run.py
import sys
import os

# Додаємо поточну папку в шляхи пошуку (щоб Python бачив папку src)
sys.path.append(os.getcwd())

from src.ai.client import get_model


def main():
    print("🚀 1. Ініціалізація моделі...")
    try:
        model = get_model()
        print("✅ Модель завантажено.")

        print("📡 2. Відправка тестового запиту до Google Gemini...")
        # Простий запит, щоб перевірити JSON режим
        response = model.generate_content(
            "Назви 3 популярні криптовалюти. Поверни лише JSON формат: [{\"name\": \"...\", \"symbol\": \"...\"}]"
        )

        print("🎉 3. Відповідь отримано!")
        print("-" * 20)
        print(response.text)
        print("-" * 20)

    except Exception as e:
        print(f"❌ ПОМИЛКА: {e}")
        print("Порада: Перевірте ваш GOOGLE_API_KEY у файлі .env")


if __name__ == "__main__":
    main()