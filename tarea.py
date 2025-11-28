import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os

load_dotenv()

CONTACTO = os.getenv("CONTACTO")
MENSAJE = os.getenv("MENSAJE")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://web.whatsapp.com")
        print("Escanea el QR...")

        await page.wait_for_selector("div[contenteditable='true'][data-tab='3']", timeout=60000)

        await page.fill("div[contenteditable='true'][data-tab='3']", CONTACTO)
        await page.wait_for_selector(f"span[title='{CONTACTO}']")
        await page.click(f"span[title='{CONTACTO}']")

        await page.wait_for_selector("div[contenteditable='true'][data-tab='10']")
        await page.fill("div[contenteditable='true'][data-tab='10']", MENSAJE)
        await page.keyboard.press("Enter")

        await page.wait_for_timeout(3000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
