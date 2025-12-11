"""
main.py
Automates sending messages through WhatsApp Web using Playwright and Python.

This script:
- Opens WhatsApp Web using Chromium.
- Maintains a persistent session to avoid scanning the QR code every time.
- Reads the contact and message from .env.
- Is compatible with direct execution or execution through Apache Airflow using an async function.

"""

import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from whatsapp_agent.path import PROJECT_ROOT

load_dotenv(PROJECT_ROOT / "example.env")

CONTACT_NAME = os.getenv("CONTACT")
MESSAGE_TEXT = os.getenv("MESSAGE")

# Basic validation
if not CONTACT_NAME or not MESSAGE_TEXT:
    raise ValueError("Missing CONTACT or MESSAGE in example.env")

async def main():
    """
    Main flow that controls WhatsApp Web automation.
    - Launches Chromium with a persistent session.
    - Opens WhatsApp Web.
    - If no previous session exists → requests QR scanning.
    - Searches for the contact and sends the specified message.
    """

    async with async_playwright() as p:

        # Keeps the session saved between executions
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False  # Visible mode to see automation progress (can be True)
        )

        page = await browser.new_page()
        await page.goto("https://web.whatsapp.com")

        # Detect if this is the first run (no "Default" folder exists)
        first_time = not (SESSION_DIR / "Default").exists()

        if first_time:
            print("🔵 Scan the QR code to log in to WhatsApp Web...")
            await page.wait_for_selector(
                "div[aria-label='Chat list']",
                timeout=120000
            )
            print("✅ Session started and saved.")
        else:
            print("🔄 Session loaded successfully.")

        # Wait for the search bar
        print("⏳ Waiting for search bar...")
        await page.wait_for_selector("div[role='textbox']", timeout=60000)

        # Search contact
        search_box = page.locator("div[role='textbox']").first
        await search_box.click()
        await search_box.fill("")  # Clear box
        await search_box.type(CONTACT_NAME, delay=40)
        await page.keyboard.press("Enter")

        # Open chat
        print(f"🔍 Looking for chat with contact '{CONTACT_NAME}'...")
        await page.wait_for_selector(f"span[title='{CONTACT_NAME}']", timeout=20000)
        await page.click(f"span[title='{CONTACT_NAME}']")

        # Send message
        print("✉️ Sending message...")

        message_box = page.locator("div[role='textbox']").last
        await message_box.click()
        await message_box.type(MESSAGE_TEXT, delay=25)
        await page.keyboard.press("Enter")

        print("✅ Message sent successfully.")

        # Wait a moment before closing the browser
        await asyncio.sleep(2)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
