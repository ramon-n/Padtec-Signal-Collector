import asyncio
import os
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

# Configuracoes de Base (NMS Central)
NMS_URL = os.getenv("TM800_URL", "http://10.144.198.10")
USERNAME = os.getenv("TM800_USER", "acesso")
PASSWORD = os.getenv("TM800_PASS", "r2riBoh8M23D")

async def collect_signals(target_node_name=None, user=None, passwd=None):
    """
    NMS Plus v4.4.12: Versão Final Estabilizada para Auditoria de Trecho.
    """
    target_user = user or USERNAME
    target_pass = passwd or PASSWORD
    central_url = NMS_URL if NMS_URL.startswith("http") else f"http://{NMS_URL}"

    # Termo de busca (IP ou parte do nome)
    ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', target_node_name)
    search_term = ip_match.group(1) if ip_match else target_node_name

    async with async_playwright() as p:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] Iniciando Auditoria NMS Plus v4.4.12...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        
        try:
            # 1. LOGIN
            await page.set_viewport_size({"width": 1400, "height": 900})
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] Login em {central_url}...")
            await page.goto(f"{central_url}/login", timeout=90000)
            await page.locator('input[placeholder*="Usu"]').first.fill(target_user)
            await page.locator('input[placeholder*="Sen"]').first.fill(target_pass)
            await page.click('button:has-text("Entrar")')
            await asyncio.sleep(20)

            # 2. FECHAR POPUPS (OBRIGATORIO)
            try:
                confirm_btn = page.locator('button:has-text("Confirmar"), .v-btn').filter(has_text="Confirmar").first
                if await confirm_btn.is_visible(timeout=8000):
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] Fechando popup detectado...")
                    await confirm_btn.click(force=True)
                    await asyncio.sleep(3)
            except: pass

            # 3. BUSCA SUPERIOR
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] Buscando site: {search_term}")
            search_input = page.locator('input[placeholder*="Buscar Elementos"], .v-text-field input').first
            await search_input.click(force=True)
            await search_input.fill(search_term)
            await page.keyboard.press("Enter")
            await asyncio.sleep(12)

            # 4. SELECIONAR RESULTADO (DROPDOWN OU LISTA)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] Selecionando site nos resultados...")
            # Tentamos clicar no item da lista que aparece com o nome do site
            # Geralmente é um .v-list-item ou similar que aparece abaixo da busca
            site_clicked = False
            
            # Contextos para busca do resultado
            for ctx in [page] + page.frames:
                try:
                    # Seletor baseado no print: o resultado da busca superior gera uma lista flutuante
                    res_el = ctx.locator('.v-list-item, .v-list-item__title').filter(has_text=search_term).first
                    if await res_el.is_visible(timeout=5000):
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] Resultado encontrado! Clicando...")
                        await res_el.click(force=True)
                        site_clicked = True
                        break
                except: continue
                
            if not site_clicked:
                # Fallback: clica em qualquer texto que contenha o termo de busca
                try:
                    await page.get_by_text(search_term).first.click(force=True, timeout=5000)
                    site_clicked = True
                except: pass

            await asyncio.sleep(8) # Tempo para o site carregar no centro

            # 5. LOCALIZAR CANAL CH35
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] Buscando Canal CH35...")
            channel_clicked = False
            # O canal CH35 pode estar em uma aba lateral ou no painel de detalhes
            for ctx in [page] + page.frames:
                try:
                    ch = ctx.locator('.v-treeview-node__label, span, div, h4').filter(has_text="CH35").first
                    if await ch.is_visible(timeout=10000):
                        await ch.click(force=True)
                        channel_clicked = True
                        break
                except: continue
            
            if not channel_clicked:
                 print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] Canal nao visivel. Forcando busca por 'CH35'...")
                 # Busca especifica pelo canal se o site ja estiver focado
                 await search_input.click(force=True)
                 await search_input.fill("CH35")
                 await page.keyboard.press("Enter")
                 await asyncio.sleep(8)
                 for ctx in [page] + page.frames:
                    try:
                        ch = ctx.locator('.v-treeview-node__label, span, div').filter(has_text="CH35").first
                        if await ch.is_visible(timeout=5000):
                            await ch.click(force=True)
                            channel_clicked = True
                            break
                    except: continue

            print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] Canal selecionado. Extraindo performance...")
            await asyncio.sleep(15)

            # 6. EXTRACAO RECURSIVA (COM AJUSTE DE CHAVES v4.4.12)
            data = {"timestamp": datetime.now().isoformat(), "equipment": target_node_name, "status": "success", "lines": {}}
            labels = ["Pin", "Pout", "OSNR", "Fator Q", "Modo"]
            signals = {}
            for l in labels:
                val = "N/A"
                for ctx in [page] + page.frames:
                    try:
                        js = f"""(label) => {{
                            try {{
                                const elements = Array.from(document.querySelectorAll('div, span, td, b, p, h4, .v-list-item__subtitle, .v-card__title'));
                                const el = elements.find(e => e.innerText.trim().toUpperCase().includes(label.toUpperCase()));
                                if (!el) return null;
                                const context = el.closest('div, section, table, tr, .v-card, .v-list-item') || el;
                                const text = context.innerText;
                                const regex = new RegExp(label + "[^0-9-]*([-+]?[0-9]*\\\\.?[0-9]+[ ]?(dBm|dB|dBQ|nm)?)", "i");
                                const match = text.match(regex);
                                if (match) return match[1].trim();
                                if (el.nextElementSibling) return el.nextElementSibling.innerText.trim();
                                return null;
                            }} catch (e) {{ return null; }}
                        }}"""
                        res = await ctx.evaluate(js, l)
                        if res: 
                            val = res
                            break
                    except: continue
                signals[l] = val

            data["lines"] = {"CH35 - Auditoria": signals}
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] Sucesso Total v4.4.12!")
            return data

        except Exception as e:
            msg = f"Erro v4.4.12: {str(e)}"
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [VERBOSE] {msg}")
            await page.screenshot(path=f"fail_v4412_{search_term}.png")
            return {"status": "error", "message": msg}
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(collect_signals("CEM-TLP-10.147.198.201-CONECT-TUDDO"))
