import urllib.request
import json
import time

def test_path_audit():
    url = "http://127.0.0.1:8000/collect_path"
    payload = {
        "path_name": "TUDDO",
        "user": "acesso",
        "pass": "r2riBoh8M23D"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    print("Iniciando auditoria simulada do trecho TUDDO (CEM-TLP -> JFA -> RJO)...")
    start = time.time()
    
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            res_body = response.read().decode('utf-8')
            elapsed = time.time() - start
            out = json.loads(res_body)
            
            print(f"Auditoria finalizada em {elapsed:.2f} segundos.")
            print(json.dumps(out, indent=4))
            
            if out.get("status") == "success":
                print("\n✅ AUDITORIA DE TRECHO COMPLETA!")
                for node in out['data']:
                    print(f"\nNó: {node['node_name']}")
                    for line, params in node['lines'].items():
                        print(f"  {line}: Pin={params['Pin']}, Q={params.get('Fator Q', 'N/A')}, Mode={params['Modo']}")
            else:
                print(f"\n❌ FALHA NA AUDITORIA: {out.get('message')}")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {e}")

if __name__ == "__main__":
    test_path_audit()
