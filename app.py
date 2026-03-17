from flask import Flask, render_template, request, jsonify
import asyncio
from datetime import datetime
from collector import collect_signals

app = Flask(__name__)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():
    return render_template('v40.html')

@app.route('/collect_path', methods=['POST'])
def collect_path():
    data = request.json
    path_name = data.get('path_name', 'TUDDO')
    
    # Configuração do trecho TUDDO conforme solicitado pelo usuário
    path_config = [
        {"ip": "10.147.198.201", "name": "CEM-TLP"},
        {"ip": "10.147.113.200", "name": "JFA"},
        {"ip": "10.147.83.201", "name": "RJO"}
    ]
    
    print(f"\n[{datetime.now()}] >>> Iniciando Auditoria de Trecho: {path_name}")
    
    results = []
    user = data.get('user')
    password = data.get('pass')
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        for node in path_config:
            print(f"Auditando Nó: {node['name']} ({node['ip']})...")
            # Coleta individual para cada nó do trecho
            res = loop.run_until_complete(collect_signals(node['ip'], user, password))
            res['node_name'] = node['name']
            results.append(res)
            
        loop.close()
        return jsonify({"status": "success", "path": path_name, "data": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    url = data.get('url')
    user = data.get('user')
    password = data.get('pass')

    print(f"\n[{datetime.now()}] >>> Nova requisição de coleta recebida!")
    print(f"URL: {url}")
    print(f"Usuário: {user}")

    if not url.startswith('http'):
        url = f"http://{url}"

    try:
        print("Iniciando loop de eventos asyncio...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        print("Chamando collect_signals no collector.py...")
        result = loop.run_until_complete(collect_signals(url, user, password))
        
        print(f"Coleta finalizada com status: {result.get('status')}")
        loop.close()
        return jsonify(result)
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"ERRO CRÍTICO NO BACKEND:\n{error_detail}")
        return jsonify({"status": "error", "message": str(e), "detail": error_detail})

if __name__ == '__main__':
    print("Iniciando interface gráfica em http://localhost:8000")
    app.run(port=8000, debug=False)
