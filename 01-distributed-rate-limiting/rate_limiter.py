import logging
import time
from typing import Optional

from redis import ConnectionError as RedisConnectionError
from redis import Redis

# Configuração de Logs
logger = logging.getLogger("RateLimiter")
logging.basicConfig(level=logging.INFO)


class DistributedRateLimiter:
    """
    Controlador de taxa de requisições distribuído usando Redis.
    Implementa o algoritmo de Janela Fixa (Fixed Window Counter) para alta performance O(1).
    """

    def __init__(self, redis_client: Redis, key_prefix: str = "rl"):
        self.redis = redis_client
        self.prefix = key_prefix

    def is_allowed(
        self, identifier: str, limit: int, window_seconds: int
    ) -> bool:
        """
        Verifica atomicamente se o cliente pode realizar a requisição.

        Args:
            identifier: Identificador único do cliente (IP, UserID, API Key).
            limit: Número máximo de requisições permitidas na janela.
            window_seconds: Tamanho da janela de tempo em segundos.

        Returns:
            bool: True se permitido, False se bloqueado.
        """
        # Cria uma chave baseada no tempo atual (janela de tempo)
        current_window = int(time.time() // window_seconds)
        key = f"{self.prefix}:{identifier}:{current_window}"

        try:
            # Pipeline garante que os comandos sejam enviados em um único RTT (Round Trip Time)
            pipe = self.redis.pipeline()
            pipe.incr(key)
            pipe.expire(
                key, window_seconds + 1
            )  # Expira a chave para não sujar a RAM
            result = pipe.execute()

            request_count = result[0]

            if request_count > limit:
                logger.warning(
                    f"Bloqueio de Rate Limit: {identifier} ({request_count}/{limit})"
                )
                return False

            return True

        except RedisConnectionError as e:
            # Fail Open: Se o Redis cair, não bloqueamos o usuário, mas alertamos a infra.
            logger.critical(f"FALHA NO REDIS (Rate Limiter inoperante): {e}")
            return True
        except Exception as e:
            logger.error(f"Erro inesperado no Rate Limiter: {e}")
            # Em caso de erro de código, bloqueamos por segurança ou liberamos?
            # Enterprise: Fail Open para disponibilidade.
            return True
