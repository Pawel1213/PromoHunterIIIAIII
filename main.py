import os
import sys
import time
from src.chat_bot import bot  # <--- ІМПОРТУЄМО ВАШОГО РОЗУМНОГО БОТА

# ==================== LOCK МЕХАНІЗМ ====================
# Цей блок гарантує, що бот запущений лише в одному екземплярі

LOCK_FILE = "/tmp/promohunter_bot.lock"

def acquire_lock():
    """Отримати lock - гарантує один екземпляр бота"""
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, 'r') as f:
                old_pid_str = f.read().strip()
            
            if old_pid_str.isdigit():
                old_pid = int(old_pid_str)
                # Перевірити чи старий процес ще живий
                try:
                    os.kill(old_pid, 0) # Сигнал 0 нічого не робить, але перевіряє чи існує процес
                    print(f"❌ Бот вже працює з PID {old_pid}")
                    print("⚠️ Зупиняю запуск, щоб уникнути Error 409 Conflict.")
                    sys.exit(1)
                except OSError:
                    print(f"⚠️ Lock-файл існує, але процес {old_pid} мертвий. Перезаписуємо.")
        except Exception as e:
            print(f"⚠️ Помилка читання lock-файлу: {e}")

    # Записати новий PID (наш поточний номер процесу)
    try:
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        print(f"✅ Lock отримано. PID: {os.getpid()}")
    except Exception as e:
        print(f"❌ Не вдалося створити LOCK_FILE: {e}")

def release_lock():
    """Звільнити lock при завершенні"""
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
            print("✅ Lock звільнено")
    except Exception as e:
        print(f"⚠️ Не вдалося видалити LOCK_FILE: {e}")

# ==================== ЗАПУСК ====================

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 ЗАПУСК PromoHunter Bot (Main Wrapper)")
    print("=" * 50)

    # 1. Включаємо захист від двійників
    acquire_lock()

    try:
        # 2. Видаляємо вебхук (щоб точно працював polling)
        bot.remove_webhook()
        
        # 3. Запускаємо бота
        print("🔄 Polling started... (Натисніть Ctrl+C для зупинки)")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)

    except KeyboardInterrupt:
        print("\n⏹️ Зупинено користувачем.")
    except Exception as e:
        print(f"\n❌ Критична помилка: {e}")
    finally:
        # 4. При виході - видаляємо файл-замок
        release_lock()
