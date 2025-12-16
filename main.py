import os

import time

import sys

import telebot

from telebot import apihelper

from src.chat_bot import bot  # Імпортуємо нашого бота



# ==================== НАЛАШТУВАННЯ ====================

RETRY_DELAY = 10  # Скільки секунд чекати перед повторною спробою, якщо є конфлікт

MAX_RETRIES = 5   # Скільки разів пробувати перезапуститись



def run_bot():

    print("=" * 50)

    print("🚀 ЗАПУСК PromoHunter Bot (Smart Wrapper)")

    print("=" * 50)



    # 1. Видаляємо вебхук (обов'язково для Polling)

    try:

        bot.remove_webhook()

        print("✅ Вебхук видалено.")

    except Exception as e:

        print(f"⚠️ Помилка видалення вебхуку: {e}")



    # 2. Цикл запуску з обробкою конфліктів

    attempt = 0

    while True:

        try:

            print("🔄 Запускаю polling...")

            bot.infinity_polling(timeout=60, long_polling_timeout=60)

            

            # Якщо infinity_polling завершився сам без помилок (рідкість)

            break 



        except apihelper.ApiTelegramException as e:

            if e.error_code == 409:

                # ЦЕ САМЕ ВАША ПОМИЛКА

                attempt += 1

                print(f"\n❌ КОНФЛІКТ (Error 409): Стара версія бота все ще працює.")

                print(f"⏳ Чекаю {RETRY_DELAY} секунд, поки старий процес завершиться... (Спроба {attempt}/{MAX_RETRIES})")

                time.sleep(RETRY_DELAY)

                

                if attempt > MAX_RETRIES:

                    print("💀 Не вдалося захопити контроль над ботом. Зупинка.")

                    sys.exit(1)

            else:

                # Інші помилки Telegram

                print(f"❌ Помилка API Telegram: {e}")

                time.sleep(5)

                

        except Exception as e:

            print(f"❌ Критична помилка: {e}")

            time.sleep(5)

            # Перезапуск циклу

            print("🔄 Перезапуск через 5 сек...")

            time.sleep(5)



if __name__ == "__main__":

    run_bot()

 
