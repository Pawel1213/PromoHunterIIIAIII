# Файл: main.py
# Це "міст", який запускає бота
from src.chat_bot import bot

if __name__ == "__main__":
    print("🚀 Запуск PromoHunter Bot через main.py...")
    # Запускаємо бота з параметрами стабільності
    bot.infinity_polling(timeout=60, long_polling_timeout=60)