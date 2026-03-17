import asyncio
import os
import json
from datetime import datetime
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

# Configurações do TM800
BASE_URL = os.getenv("TM800_URL", "http://10.144.198.10")
USERNAME = os.getenv("TM800_USER", "admin")
PASSWORD = os.getenv("TM800_PASS", "admin")

async def collect_signals(url=None, user=None, passwd=None):
    # Fallback para .env se não for passado via argumento
    target_url = url or os.getenv("TM800_URL", "http://10.144.198.10")
    target_user = user or os.getenv("TM800_USER", "admin")
    target_pass = passwd or os.getenv("TM800_PASS", "admin")

    async with async_playwright() as p:
        if not target_url.startswith("http"):
            target_url = f"http://{target_url}"
            
        # Iniciando o navegador (Headless=False para depuração visual se necessário)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(ignore_https_errors=True)
        context.set_default_timeout(90000)
        page = await context.new_page()
        print(f"[{datetime.now()}] Acessando {target_url}/login...")
        try:
            await page.set_viewport_size({"width": 1280, "height": 800})
            await page.goto(f"{target_url}/login", timeout=90000)
            
            # Login
            print("Realizando login...")
            await page.fill('input[placeholder="Usuário"]', target_user)
            await page.fill('input[placeholder="Senha"]', target_pass)
            await page.click('button:has-text("Entrar")')
            
            # Aguarda a página carregar
            await asyncio.sleep(5)
            await page.wait_for_load_state("networkidle", timeout=60000)
            print("Login realizado. Verificando popups...")

            # Tratamento de Popup de Licença (Imagem do diagnóstico)
            try:
                # Tenta várias formas de encontrar o botão "Confirmar"
                confirm_btn = page.get_by_text("Confirmar", exact=False).first
                if await confirm_btn.is_visible(timeout=10000):
                    print("Popup de licença detectado. Forçando fechamento...")
                    await confirm_btn.click(force=True)
                    await asyncio.sleep(2)
            except:
                pass

            # Busca Direta pelo Equipamento (Barra de busca no topo)
            print("Buscando equipamento na barra de busca...")
            try:
                # Localiza a barra de busca
                search_input = page.locator('input[placeholder*="Buscar"], .v-text-field input').first
                await search_input.click(force=True)
                await search_input.fill("TM800")
                await page.keyboard.press("Enter")
                await asyncio.sleep(8)
                await page.screenshot(path="debug_search_results.png")
                
                # Tenta localizar qualquer item que pareça um resultado de busca contendo TM800
                # No NMS+, resultados costumam aparecer em listas suspensas (v-list-item)
                print("Aguardando lista de resultados...")
                tm800_selector = page.locator('.v-list-item, .v-list-item__title, [role="option"]').filter(has_text="TM800").first
                await tm800_selector.wait_for(state="visible", timeout=10000)
                await tm800_selector.click(force=True)
                print("Equipamento selecionado com sucesso via busca.")
            except Exception as e:
                print(f"Falha na busca/seleção: {e}. Tentando via menu lateral...")
                await page.screenshot(path="debug_search_failed.png")
                # Fallback: Clique no menu hambúrguer (ícone de 3 barras)
                try:
                    await page.locator('.v-app-bar__nav-icon, i.mdi-menu, button:has(i.mdi-menu)').click(force=True)
                    await asyncio.sleep(2)
                    await page.click('text="Gerenciamento de NEs"', force=True)
                    await page.click('text="Árvore de Equipamentos"', force=True)
                    await asyncio.sleep(5)
                    await page.screenshot(path="debug_tree_manual.png")
                    await page.click('text="TM800"', force=True, timeout=15000)
                except Exception as e2:
                    print(f"Falha total na localização: {e2}")
                    raise

            await asyncio.sleep(5)
            await page.wait_for_load_state("networkidle", timeout=30000)
            print("Extraindo dados avançados...")
            
            data = {
                "timestamp": datetime.now().isoformat(),
                "equipment": "TM800 Device",
                "status": "success",
                "lines": {}
            }
            
            lines_data = {}
            # Coletamos para LINE 1 e LINE 2 por padrão, mas o robô buscará os parâmetros específicos
            for line_idx in [1, 2]:
                line_label = f"LINE {line_idx}"
                print(f"Coletando {line_label}...")
                
                async def get_advanced_value(label):
                    try:
                        return await page.evaluate(f"""(args) => {{
                            try {{
                                const label = args[0];
                                const elements = Array.from(document.querySelectorAll('div, span, td, b, p, h4, .v-list-item__subtitle'));
                                // Busca exata ou parcial pelo label
                                const labelEl = elements.find(e => {{
                                    const text = e.innerText.trim();
                                    return text.toLowerCase() === label.toLowerCase() || 
                                           (text.includes(label) && text.length < label.length + 5);
                                }});
                                
                                if (!labelEl) return 'N/A';
                                
                                // Tenta achar o valor no contêiner pai mais próximo
                                const context = labelEl.closest('div, section, table, tr, .v-card, .v-list-item');
                                if (context) {{
                                    const text = context.innerText;
                                    // Regex para diferentes formatos (ex: "Pin -5.96 dBm" ou "OSNR 22.90 dB")
                                    const regex = new RegExp(label + "[^0-9-]*([-+]?[0-9]*\\\\.?[0-9]+[ ]?(dBm|dB|dBQ|nm)?)", "i");
                                    const match = text.match(regex);
                                    if (match) return match[1].trim();
                                    
                                    // Fallback: se houver um elemento irmão com o valor
                                    if (labelEl.nextElementSibling) return labelEl.nextElementSibling.innerText.trim();
                                }}
                                return 'N/A';
                            }} catch (e) {{ return 'ERR'; }}
                        }}""", [label])
                    except: return "ERR"

                lines_data[line_label] = {
                    "Pin": await get_advanced_value("Pin"),
                    "Pout": await get_advanced_value("Pout"),
                    "OSNR": await get_advanced_value("OSNR"),
                    "Fator Q": await get_advanced_value("Fator Q"),
                    "Modo": await get_advanced_value("Modo")
                }

            data["lines"] = lines_data
            
            # Exportação
            if not os.path.exists("data_exports"): os.makedirs("data_exports")
            output_file = os.path.join("data_exports", f"audit_{datetime.now().strftime('%H%M%S')}.json")
            with open(output_file, "w") as f: json.dump(data, f, indent=4)
            
            return data

        except Exception as e:
            error_msg = f"Erro durante a coleta: {e}"
            print(error_msg)
            await page.screenshot(path="error_debug.png")
            return {"status": "error", "message": error_msg}
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(collect_signals())
