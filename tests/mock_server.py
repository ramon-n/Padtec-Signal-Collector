from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Template para a página de login (Baseado na imagem 1)
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Padtec nms plus - Login</title>
    <style>
        body { font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f5f5f5; }
        .login-box { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 400px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #f2a68d; border: none; color: white; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="login-box">
        <h1 style="color: #444;">Padtec nms </h1>
        <form action="/login" method="post">
            <input type="text" name="user" placeholder="Usuário">
            <input type="password" name="pass" placeholder="Senha">
            <button type="submit">Entrar</button>
        </form>
    </div>
</body>
</html>
"""

# Template para o menu e a árvore (Baseado na imagem 2 e 3)
MAIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Padtec nms plus</title>
    <style>
        body { margin: 0; display: flex; }
        .sidebar { width: 250px; background: #333; color: white; height: 100vh; padding: 20px; }
        .content { flex-grow: 1; padding: 20px; }
        .tree-node { cursor: pointer; padding: 5px; }
        .tree-node:hover { background: #444; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h3>Menu Principal</h3>
        <div id="gerenciamento-nes">
            <b>Gerenciamento de NEs</b>
            <div style="margin-left: 20px;">
                <div class="tree-node" id="arvore-link">Árvore de Equipamentos</div>
            </div>
        </div>
    </div>
    <div class="content" id="main-content">
        <h1>Bem-vindo</h1>
        <div id="tree-container" style="display: none;">
            <h3>Árvore de Equipamentos</h3>
            <ul>
                <li>Fisico
                    <ul>
                        <li class="tree-node" id="tm800-link">TM800G-LT#2032</li>
                    </ul>
                </li>
            </ul>
        </div>
        <div id="ports-view" style="display: none;">
            <h3>Portas - TM800G-LT#2032</h3>
            <div style="display: flex; gap: 20px;">
                <div class="port-box">
                    <h4>LINE 1</h4>
                    <div>Pin: <span id="pin1">-12.50 dBm</span></div>
                    <div>Pout: <span id="pout1">2.30 dBm</span></div>
                </div>
                <div class="port-box">
                    <h4>LINE 2</h4>
                    <div>Pin: <span id="pin2">-14.10 dBm</span></div>
                    <div>Pout: <span id="pout2">1.80 dBm</span></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('arvore-link').onclick = () => {
            document.getElementById('tree-container').style.display = 'block';
        };
        document.getElementById('tm800-link').onclick = () => {
            document.getElementById('ports-view').style.display = 'block';
            document.getElementById('tree-container').style.display = 'none';
        };
    </script>
</body>
</html>
"""

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/main')
    return render_template_string(LOGIN_HTML)

@app.route('/main')
def main():
    return render_template_string(MAIN_HTML)

if __name__ == '__main__':
    app.run(port=5000)
