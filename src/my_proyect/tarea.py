import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env
load_dotenv()

# Obtiene el nombre del contacto y el mensaje desde el .env
CONTACT_NAME = os.getenv("CONTACTO")
MESSAGE_TEXT = os.getenv("MENSAJE")

# Verifica que las variables existan
if not CONTACT_NAME or not MESSAGE_TEXT:
    raise ValueError(
        "No se encontró el contacto el mensaje, por ello no se puede enviar."
    )

async def main():
    async with async_playwright() as p:
        # Abre el navegador
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        # Abre WhatsApp Web
        await page.goto("https://web.whatsapp.com")
        print("Escanea el QR para iniciar sesión...")
        # Espera que cargue la barra de búsqueda de contactos
        await page.wait_for_selector("div[contenteditable='true'][data-tab='3']", timeout=60000)
        # Escribe el nombre del contacto en la búsqueda
        await page.fill("div[contenteditable='true'][data-tab='3']", CONTACT_NAME)
        # Espera a que aparezca el contacto y lo selecciona
        await page.wait_for_selector(f"span[title='{CONTACT_NAME}']")
        await page.click(f"span[title='{CONTACT_NAME}']")
        # Espera que aparezca el campo para escribir mensajes
        await page.wait_for_selector("div[contenteditable='true'][data-tab='10']")
        # Escribe el mensaje
        await page.fill("div[contenteditable='true'][data-tab='10']", MESSAGE_TEXT)
        # Envía el mensaje
        await page.keyboard.press("Enter")
        # Espera un momento antes de cerrar
        await page.wait_for_timeout(3000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
