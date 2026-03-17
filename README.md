# Padtec Signal Collector v3.2

Automação inteligente para coleta de dados de potência (Pin/Pout) em equipamentos Padtec TM800 via interface NMS+.

## 🚀 Funcionalidades

- **Interface Web Moderna**: GUI intuitiva construída com Flask e Vuetify/Vanilla CSS.
- **Motor de Coleta Ultra-Resiliente**: Baseado em Playwright com suporte a:
  - Fechamento automático de popups de licença/sistema.
  - Busca rápida de elementos de rede (contornando a lentidão da árvore de equipamentos).
  - Cliques forçados para máxima compatibilidade em redes industriais.
- **Exportação de Dados**: Salvamento automático em formato JSON na pasta `data_exports`.
- **Modo Autônomo**: Suporte a variáveis de ambiente (`.env`) para operação sem intervenção manual.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.12
- **Web Framework**: Flask
- **Automação**: Playwright (Chromium)
- **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript (Async/Fetch)

## 📋 Pré-requisitos

1. Python 3.12+ instalado.
2. Acesso à rede onde se encontra o NMS+ da Padtec.

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd Padtec
   ```

2. Instale as dependências:
   ```powershell
   & "C:\Users\ramon\AppData\Local\Programs\Python\Python312\python.exe" -m pip install flask flask-cors playwright python-dotenv
   ```

3. Instale o navegador do Playwright:
   ```powershell
   & "C:\Users\ramon\AppData\Local\Programs\Python\Python312\python.exe" -m playwright install chromium
   ```

## 🚀 Como Usar (Início Rápido)

1. Vá até a pasta `Padtec`.
2. Dê dois cliques no arquivo **`iniciar.bat`**.
3. O servidor subirá e o navegador abrirá automaticamente em `http://localhost:8000`.

*Alternativamente, você pode rodar via terminal:*
```powershell
& "C:\Users\ramon\AppData\Local\Programs\Python\Python312\python.exe" start.py
```

## 📁 Estrutura do Projeto

- `app.py`: Servidor Flask e rotas da API.
- `collector.py`: Lógica principal de automação e raspagem.
- `templates/`: Interface visual (HTML/CSS).
- `data_exports/`: Histórico de coletas em JSON.
- `.env`: Configurações de credenciais (Ignorado pelo Git).

## 🛡️ Segurança

Credenciais sensíveis devem ser mantidas no arquivo `.env`. Nunca submeta o arquivo `.env` para repositórios públicos.

---
**Desenvolvido por Antigravity AI para Padtec Automation.**
