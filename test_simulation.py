# Файл: test_simulation.py
import asyncio
from src.ai.client import get_model

# 1. СТВОРЮЄМО "ФЕЙКОВИЙ" HTML (Симуляція успішного скачування)
# Уявіть, що Hunter зміг це скачати з реального сайту.
SIMULATED_HTML = """
<html>
<body>
    <h1>Top 3 Crypto Casinos for 2025</h1>

    <div class="casino-card">
        <h2>1. MegaBull Casino</h2>
        <p class="offer">Exclusive Welcome Offer: <strong>200% up to 5 BTC</strong> + 50 Free Spins.</p>
        <small>Wagering requirements: 35x bonus amount.</small>
    </div>

    <div class="casino-card">
        <h2>2. LuckyWhale.io</h2>
        <p class="offer">Get a massive 100% Deposit Match up to 1 ETH.</p>
        <small>Terms: 40x rollover apply.</small>
    </div>

    <div class="casino-card">
        <h2>3. MoonSpin</h2>
        <p class="offer">No deposit bonus: 20 Free Spins on registration!</p>
        <small>Wager: 10x only.</small>
    </div>
</body>
</html>
"""


async def main():
    print("🧪 ЗАПУСК СИМУЛЯЦІЇ...")
    print(f"📄 Вхідні дані: HTML сторінка ({len(SIMULATED_HTML)} символів)")

    # 2. АНАЛІЗ ЧЕРЕЗ GEMINI 2.0
    print("\n🧠 AI: Аналізую структуру...")
    model = get_model()

    prompt = f"""
    Analyze this HTML snippet. Extract crypto casino bonuses.
    Return strictly JSON format:
    [
        {{
            "casino_name": "Name",
            "bonus_offer": "Bonus details",
            "wagering": "Wagering requirements"
        }}
    ]

    HTML:
    {SIMULATED_HTML}
    """

    try:
        response = model.generate_content(prompt)
        print("\n🎉 РЕЗУЛЬТАТ (Це те, що ми будемо записувати в базу):")
        # Прибираємо зайві символи форматування, якщо вони є
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        print(clean_json)

    except Exception as e:
        print(f"❌ AI Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())