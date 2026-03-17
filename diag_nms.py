import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

async def debug_nms_layout():
    async with async_playwright() as p:
        print("Iniciando Diagnostico de Layout NMS Plus...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        await page.set_viewport_size({"width": 1400, "height": 900})
        
        url = os.getenv("TM800_URL", "http://10.144.198.10")
        if not url.startswith("http"): url = f"http://{url}"
        
        await page.goto(f"{url}/login", wait_until="networkidle")
        await page.fill('input[placeholder="Usuário"]', os.getenv("TM800_USER", "acesso"))
        await page.fill('input[placeholder="Senha"]', os.getenv("TM800_PASS", "r2riBoh8M23D"))
        await page.click('button:has-text("Entrar")')
        
        await asyncio.sleep(10)
        print("Screnshot do Dashboard pos-login...")
        await page.screenshot(path="diag_nms_dashboard.png")
        
        # Procura por iframes
        iframes = page.frames
        print(f"Total de iframes detectados: {len(iframes)}")
        for i, frame in enumerate(iframes):
            print(f"Frame {i}: {frame.name} - {frame.url}")
            
        # Tenta achar o texto "Procurar" no DOM
        content = await page.content()
        with open("diag_nms_dom.txt", "w", encoding="utf-8") as f:
            f.write(content)
            
        await browser.close()
        print("Diagnostico concluido. Verifique diag_nms_dashboard.png e diag_nms_dom.txt")

if __name__ == "__main__":
    asyncio.run(debug_nms_layout())
