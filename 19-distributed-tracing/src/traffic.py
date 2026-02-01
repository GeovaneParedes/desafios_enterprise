import requests
import time

print("🔫 Disparando requisições para gerar traces...")
for i in range(10):
    try:
        resp = requests.get("http://localhost:5000/checkout")
        print(f"Req {i+1}: {resp.status_code} - {resp.elapsed.total_seconds()}s")
    except:
        print("Erro de conexão. O server está on?")
    time.sleep(1)
