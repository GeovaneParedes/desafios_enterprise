import time

import redis  # noqa

from src.limiter import RateLimiter


def run_simulation():
    # Conecta no Redis do Docker
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)

    # Regra: 5 requisições a cada 10 segundos
    limiter = RateLimiter(redis_client=r, limit=5, window_seconds=10)
    user_id = "user_123"

    print("--- 🚦 Iniciando Teste de Rate Limit ---")
    print(
        f"Regra: Máximo de {limiter.limit}"
        f"reqs a cada {limiter.window_seconds}s\n"
    )

    # Vamos tentar fazer 10 requisições seguidas
    for i in range(1, 11):
        allowed = limiter.is_allowed(user_id)

        status = "✅ PERMITIDO" if allowed else "⛔ BLOQUEADO (429)"
        print(f"Req #{i}: {status}")

        time.sleep(0.5)  # Pequena pausa para visualização

    print("\n--- ⏳ Aguardando janela expirar (10s)... ---")
    time.sleep(10)

    print("\n--- 🔄 Nova Tentativa (Nova Janela) ---")
    allowed = limiter.is_allowed(user_id)
    status = "✅ PERMITIDO" if allowed else "⛔ BLOQUEADO"
    print(f"Req #11: {status}")


if __name__ == "__main__":
    try:
        run_simulation()
    except redis.ConnectionError:
        print(
            "❌ Erro: Não foi possível conectar ao Redis."
            "Execute 'make up' primeiro."
        )
