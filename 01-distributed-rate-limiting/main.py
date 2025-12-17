from fastapi import Depends, FastAPI, HTTPException, Request
from redis import Redis

from rate_limiter import DistributedRateLimiter

# Configuração
app = FastAPI(title="Enterprise Challenge #01 - Rate Limiter")
redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)
limiter = DistributedRateLimiter(redis_client)

# Configurações de Limite (Poderiam vir de variáveis de ambiente)
LIMIT_REQUESTS = 5
WINDOW_SECONDS = 10


async def check_rate_limit(request: Request):
    """
    Dependência que valida o rate limit antes de processar a rota.
    """
    client_ip = request.client.host
    # Em produção, usaríamos X-Forwarded-For se estiver atrás de um Proxy

    allowed = limiter.is_allowed(client_ip, LIMIT_REQUESTS, WINDOW_SECONDS)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too Many Requests. Tente novamente mais tarde.",
        )


@app.get("/api/v1/resource", dependencies=[Depends(check_rate_limit)])
def get_sensitive_data():
    """Rota protegida por Rate Limit."""
    return {
        "data": "Conteúdo exclusivo e caro para processar.",
        "status": "success",
    }


@app.get("/health")
def health_check():
    """Health check não deve ter rate limit restritivo."""
    return {"status": "ok"}
