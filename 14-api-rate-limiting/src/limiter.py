import time
from datetime import datetime

import redis


class RateLimiter:
    def __init__(
        self, redis_client: redis.Redis, limit: int, window_seconds: int
    ):
        """
        Args:
            redis_client: Conexão com o Redis.
            limit: Máximo de requisições permitidas.
            window_seconds: Tamanho da janela de tempo em segundos.
        """
        self.redis = redis_client
        self.limit = limit
        self.window_seconds = window_seconds

    def is_allowed(self, user_id: str) -> bool:
        """
        Verifica se o usuário pode fazer uma requisição.
        Retorna True se permitido, False se bloqueado (Rate Limited).
        """
        # 1. Cria uma chave única baseada no tempo atual (Janela Fixa)
        # Ex: Se window=60s, a chave muda a cada minuto.
        # Int(Timestamp / Window) cria "buckets" de tempo.
        current_window = int(time.time() / self.window_seconds)
        key = f"rate_limit:{user_id}:{current_window}"

        # 2. Pipeline para executar comandos atomicamente
        pipe = self.redis.pipeline()
        pipe.incr(key)  # Incrementa o contador
        pipe.expire(
            key, self.window_seconds + 1
        )  # Define expiração (segurança)
        result = pipe.execute()

        # O resultado do INCR é o primeiro item da lista retornada pelo
        # pipeline
        request_count = result[0]

        # 3. Validação
        if request_count > self.limit:
            return False

        return True
