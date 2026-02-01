import time
import requests
import sys

BASE_URL = "http://localhost:5000"


def check_probes():
    print("\n--- 🤖 Kubelet Simulator Iniciado ---")
    print("Monitorando Probes a cada 2 segundos...\n")

    while True:
        try:
            # 1. Checa Liveness (Estou vivo?)
            try:
                live = requests.get(f"{BASE_URL}/health/live", timeout=1)
                live_status = live.status_code
            except requests.RequestException:
                live_status = 0  # Down

            # 2. Checa Readiness (Posso trabalhar?)
            try:
                ready = requests.get(f"{BASE_URL}/health/ready", timeout=1)
                ready_status = ready.status_code
            except requests.RequestException:
                ready_status = 0  # Down

            # --- DECISÃO DO ORQUESTRADOR ---

            # Lógica de Restart (Liveness)
            if live_status != 200:
                print(f"💀 [LIVENESS FALHOU] Status {live_status}."
                      f"AÇÃO: RESTART POD 🔄")
                # Na vida real, o Docker mataria o processo aqui.
                # Aqui vamos apenas alertar.

            # Lógica de Tráfego (Readiness)
            elif ready_status != 200:
                print(f"⛔ [READINESS FALHOU] Status {ready_status}."
                      f"AÇÃO: REMOVE DO LOAD BALANCER (Sem tráfego) 🛡️")

            # Tudo OK
            else:
                print("✅ [HEALTHY] Pod Saudável. AÇÃO: MANTÉM TRÁFEGO 🚀")

        except KeyboardInterrupt:
            print("\nParando simulador.")
            sys.exit(0)

        time.sleep(2)


if __name__ == "__main__":
    check_probes()
