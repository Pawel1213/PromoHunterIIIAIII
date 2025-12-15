# Файл: test_db_save.py
import sys
import os

# Додаємо шлях до папки src
sys.path.append(os.getcwd())

from src.database import save_bonus

if __name__ == "__main__":
    print("💾 Пробую зберегти тестовий бонус...")

    # Симулюємо дані, які нібито знайшов AI
    save_bonus(
        casino_name="Test Casino 777",
        bonus_offer="100 BTC Welcome Pack",
        wagering="30x"
    )