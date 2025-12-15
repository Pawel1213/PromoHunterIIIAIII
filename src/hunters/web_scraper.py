# Файл: src/hunters/web_scraper.py

import asyncio
import random
from playwright.async_api import async_playwright


class WebHunter:
    def __init__(self, headless=True):
        self.headless = headless

    async def fetch_page_content(self, url: str):
        print(f"🕷️ Hunter (Stealth): Підкрадаюсь до -> {url}")

        async with async_playwright() as p:
            # Масив аргументів, які вимикають ознаки робота
            browser_args = [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--window-position=0,0",
                "--ignore-certificate-errors",
                "--window-size=1920,1080",
            ]

            # Запускаємо браузер з аргументами
            browser = await p.chromium.launch(
                headless=self.headless,
                args=browser_args
            )

            # Створюємо контекст з реалістичним відбитком
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                locale="en-US",
                timezone_id="America/New_York"
            )

            # Додатковий скрипт для приховування webdriver прапора
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            page = await context.new_page()

            try:
                # Переходимо на сайт
                await page.goto(url, timeout=40000, wait_until="domcontentloaded")

                # Імітуємо поведінку людини (випадкова затримка)
                await page.wait_for_timeout(random.randint(3000, 5000))

                # Прокручуємо сторінку вниз (тригер завантаження контенту)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)

                # Забираємо HTML
                content = await page.content()
                print(f"✅ Hunter: Вдале полювання! Завантажено {len(content)} байт.")

                return content

            except Exception as e:
                print(f"❌ Hunter Error: Ціль втекла. Причина: {e}")
                return None

            finally:
                await browser.close()