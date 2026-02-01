import time
import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuração de Log para não poluir o terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# --- ESTADO INTERNO ---
# Simula se a aplicação está travada (Deadlock)
IS_ALIVE = True
# Simula se a aplicação conectou no banco (Startup/Dependency)
IS_READY = False


@app.route('/')
def home():
    return "Bem-vindo ao Sistema Enterprise!"

# --- PROBES (O que o Kubernetes chama) ---


@app.route('/health/live')
def liveness_probe():
    """
    O Kubernetes chama isso a cada 10s.
    Se retornar 200: Mantém o pod.
    Se retornar 500 ou Timeout: REINICIA o pod.
    """
    if IS_ALIVE:
        return jsonify(status="alive"), 200
    else:
        # Simula um estado irrecuperável
        return jsonify(status="dead"), 500


@app.route('/health/ready')
def readiness_probe():
    """
    O Kubernetes chama isso a cada 5s.
    Se retornar 200: Manda tráfego (usuários).
    Se retornar 503: Corta tráfego (aguarda voltar).
    """
    if IS_READY:
        return jsonify(status="ready"), 200
    else:
        return jsonify(
            status="not_ready", reason="Database connecting..."), 503

# --- CHAOS ENGINEERING (Para simularmos os problemas) ---


@app.route('/admin/startup')
def simulate_startup():
    global IS_READY
    time.sleep(1)  # Simula conexão
    IS_READY = True
    return "✅ Aplicação Inicializada (Banco Conectado)"


@app.route('/admin/crash_db')
def simulate_db_failure():
    global IS_READY
    IS_READY = False
    return "⚠️ Banco caiu! (Readiness vai falhar)"


@app.route('/admin/deadlock')
def simulate_deadlock():
    global IS_ALIVE
    IS_ALIVE = False
    return "💀 Deadlock simulado! (Liveness vai falhar)"


if __name__ == '__main__':
    print("🏥 App rodando na porta 5000.")
    print("   Estado Inicial: Vivo=SIM, Pronto=NÃO (Simulando boot)")
    app.run(port=5000)
