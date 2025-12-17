import time
from concurrent.futures import ThreadPoolExecutor

import requests

URL = "http://localhost:8000/api/v1/resource"
TOTAL_REQUESTS = 15


def call_api(request_id):
    """Realiza uma chamada HTTP e retorna o status code."""
    try:
        resp = requests.get(URL, timeout=2)
        print(f"[Req {request_id:02d}] Status: {resp.status_code}")
        return resp.status_code
    except Exception as e:
        print(f"[Req {request_id:02d}] Erro de conexão: {e}")
        return 0


if __name__ == "__main__":
    print(
        f"--- Iniciando Teste de Estresse ({TOTAL_REQUESTS} reqs simultâneas) ---"
    )
    print(f"Alvo: {URL}\n")

    start_time = time.time()

    # Simula usuários simultâneos batendo na API
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(call_api, range(TOTAL_REQUESTS)))

    duration = time.time() - start_time

    # Análise dos Resultados
    success_count = results.count(200)
    blocked_count = results.count(429)
    errors = len(results) - (success_count + blocked_count)

    print("\n--- Relatório Final ---")
    print(f"Tempo Total: {duration:.2f}s")
    print(f"✅ Sucessos (200 OK): {success_count}")
    print(f"🛡️ Bloqueios (429 Too Many Requests): {blocked_count}")
    print(f"❌ Erros: {errors}")

    if blocked_count > 0:
        print("\nCONCLUSÃO: O Rate Limiter está FUNCIONANDO. 🚀")
    else:
        print("\nCONCLUSÃO: FALHA. Nenhuma requisição foi bloqueada. ⚠️")
