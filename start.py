import subprocess
import time
import webbrowser
import os
import sys

def start_app():
    # Caminho do executável do Python
    python_exe = sys.executable
    
    print("🚀 Iniciando Padtec Path Monitor v4.0...")
    
    # Inicia o servidor Flask em um processo separado
    # Usamos subprocess.Popen para não bloquear a execução do script
    try:
        process = subprocess.Popen(
            [python_exe, "app.py"],
            cwd=os.getcwd()
        )
        
        # Aguarda 2 segundos para o servidor subir
        time.sleep(3)
        
        # Abre o navegador no endereço local
        url = "http://localhost:8000"
        print(f"🌍 Abrindo o navegador em {url}...")
        webbrowser.open(url)
        
        print("\n✅ Aplicação rodando!")
        print("Mantenha esta janela aberta enquanto estiver usando o monitor.")
        print("Pressione Ctrl+C para encerrar.")
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando aplicação...")
        process.terminate()
    except Exception as e:
        print(f"\n❌ Erro ao iniciar: {e}")

if __name__ == "__main__":
    start_app()
