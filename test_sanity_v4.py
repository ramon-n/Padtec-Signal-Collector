import urllib.request
import json
import time

def test_sanity_v4():
    url = "http://127.0.0.1:8000/collect"
    payload = {
        "url": "10.144.198.10",
        "user": "acesso",
        "pass": "r2riBoh8M23D"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    print("Testando Coletor v4.0 no IP padrão (10.144.198.10)...")
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res_body = response.read().decode('utf-8')
            out = json.loads(res_body)
            print(json.dumps(out, indent=4))
            if out.get("status") == "success":
                print("\n✅ MOTOR v4.0 VALIDADO!")
            else:
                print(f"\n❌ FALHA: {out.get('message')}")
    except Exception as e:
        print(f"❌ ERRO: {e}")

if __name__ == "__main__":
    test_sanity_v4()
