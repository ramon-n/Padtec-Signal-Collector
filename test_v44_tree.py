import asyncio
import os
from collector import collect_signals

async def test_nms_tree_navigation():
    print("Iniciando Teste de Navegação v4.4...")
    # Testamos com o primeiro site do trecho
    result = await collect_signals("CEM-TLP-10.147.198.201-CONECT-TUDDO")
    print("\nRESULTADO DO TESTE:")
    import json
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    asyncio.run(test_nms_tree_navigation())
