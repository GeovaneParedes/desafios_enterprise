import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from redis import Redis

from circuit_breaker import CircuitBreaker, CircuitBreakerOpenException

# Configuração
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
EXTERNAL_API_URL = "http://localhost:8001"  # URL do nosso simulador

redis_client = Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

# Instância do Circuit Breaker
# Se falhar 3 vezes, para de chamar por 10 segundos
cb_external_api = CircuitBreaker(
    redis_client=redis_client,
    service_name="external_api_v1",
    failure_threshold=3,
    recovery_timeout=10,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 API Iniciada. Circuit Breaker Armado.")
    yield
    redis_client.close()
    print("🛑 API Finalizada.")


app = FastAPI(
    title="Enterprise Challenge #04 - Circuit Breaker", lifespan=lifespan
)


async def _chamar_servico_externo():
    """Função 'perigosa' que faz a requisição HTTP real"""
    async with httpx.AsyncClient() as client:
        # Timeout curto de 2s para não travar nossa API esperando a outra
        resp = await client.get(f"{EXTERNAL_API_URL}/dados", timeout=2.0)
        resp.raise_for_status()  # Levanta erro se for 4xx ou 5xx
        return resp.json()


@app.get("/consultar")
async def consultar_dados():
    try:
        # 🛡️ Envolvemos a chamada perigosa no Circuit Breaker
        resultado = await cb_external_api.call(_chamar_servico_externo)
        return {
            "status": "sucesso",
            "origem": "API Externa",
            "dados": resultado,
        }

    except CircuitBreakerOpenException:
        # ⚡ Circuito Aberto: Fail Fast 
        # (Retorna erro imediato sem tentar conectar)
        # Em um caso real, aqui você retornaria um dado em cache ou default
        raise HTTPException(
            status_code=503,
            detail="Serviço externo instável."
                   "Tente novamente mais tarde (Circuit Open).",
        )

    except httpx.HTTPError:
        # Erro de conexão real (contabilizado pelo CB)
        raise HTTPException(
            status_code=502, detail="Erro de comunicação com serviço externo."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cb-status")
def status_circuit_breaker():
    """Rota auxiliar para ver o estado atual no Redis"""
    falhas = redis_client.get("cb:external_api_v1:failures") or 0
    is_open = redis_client.exists("cb:external_api_v1:open")
    return {
        "failures_count": int(falhas),
        "is_circuit_open": bool(is_open),
        "threshold": cb_external_api.threshold,
    }
