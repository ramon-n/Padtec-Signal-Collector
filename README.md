# Padtec Signal Collector - Optical Auditor v4.4.12

Assistente de automação para coleta de sinais em equipamentos Padtec TM800, otimizado para auditoria de trechos ópticos via **NMS Plus Central**.

## 🚀 Novidades da Versão 4.4.12
- **Auditoria NMS Plus**: Agora é possível auditar NEs que não possuem interface web própria, acessando-os via servidor central.
- **Bypass de Popups**: O robô remove automaticamente avisos de licença e popups que bloqueiam a interface.
- **Sistema Super Verbose**: Logs detalhados em tempo real no terminal para monitoramento do robô.
- **One-Click Start**: Inicialização simplificada via arquivo `.bat`.

## 🛠️ Requisitos
- Python 3.12+
- Navegador Google Chrome/Chromium 
- Acesso à rede de gerência Padtec (VPN ou Local)

## 📦 Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/ramon-n/Padtec-Signal-Collector.git
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

## ⚙️ Configuração
Edite o arquivo `.env` na raiz do projeto:
```env
TM800_URL=192.168.1.1   # IP do NMS Plus Central
TM800_USER=seu_usuario
TM800_PASS=sua_senha
```

## 🏁 Como Iniciar (Windows)
1. Dê um duplo clique no arquivo **`iniciar.bat`**.
2. O navegador abrirá automaticamente em `http://localhost:8000`.
3. Mantenha a janela preta (terminal) aberta para acompanhar o **Super Verbose**.

## 📊 Trecho TUDDO (Exemplo de Sucesso)
A aplicação está pré-configurada para auditar a rota:
- **CEM-TLP** ()
- **JFA** ()
- **RJO** ()

## 📝 Desenvolvido por
**Equipe de Especialistas (Alex, Neto, Camila, Bia, Leo, Mari)** - Focado em automação de redes ópticas de alta performance.
