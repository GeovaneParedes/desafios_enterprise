import logging
from typing import AsyncGenerator

import ujson
from fastapi import Request
from redis import Redis
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

logger = logging.getLogger("Idempotency")
logging.basicConfig(level=logging.INFO)


class IdempotencyMiddleware(BaseHTTPMiddleware):
    """
    Middleware que intercepta requisições POST para garantir idempotência.
    """

    def __init__(
        self, app, redis_client: Redis, expire_time: int = 60 * 60 * 24
    ):
        super().__init__(app)
        self.redis = redis_client
        self.expire_time = expire_time

    async def dispatch(self, request: Request, call_next):
        # 1. Filtro de verbos HTTP
        if request.method not in ["POST", "PATCH", "PUT"]:
            return await call_next(request)

        # 2. Verifica Header
        idem_key = request.headers.get("Idempotency-Key")
        if not idem_key:
            return await call_next(request)

        cache_key = f"idem:{idem_key}"

        # 3. Check Cache
        cached_response = self.redis.get(cache_key)
        if cached_response:
            logger.info(
                f"♻️  CACHE HIT: Retornando resposta salva para {idem_key}"
            )
            data = ujson.loads(cached_response)
            return JSONResponse(
                content=data["body"],
                status_code=data["status_code"],
                headers=data["headers"],
            )

        # 4. Processa a Requisição Real
        response = await call_next(request)

        # 5. Salva no Redis (Apenas Sucesso 2xx)
        if 200 <= response.status_code < 300:
            # --- CORREÇÃO DO ASYNC ITERATOR ---
            response_body = [
                section async for section in response.body_iterator
            ]
            body_content = b"".join(response_body).decode()

            async def async_iterator() -> AsyncGenerator[bytes, None]:
                for chunk in response_body:
                    yield chunk

            response.body_iterator = async_iterator()

            try:
                cache_data = {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": ujson.loads(body_content),
                }
                self.redis.setex(
                    cache_key, self.expire_time, ujson.dumps(cache_data)
                )
                logger.info(f"💾 SALVO NO REDIS: {idem_key}")
            except Exception as e:
                logger.error(f"Erro ao salvar idempotência: {e}")

        return response
