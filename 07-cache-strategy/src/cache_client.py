import os

import redis


def get_redis_client() -> redis.Redis:
    """
    Retorna uma instância configurada do cliente Redis.
    Lê configurações de variáveis de ambiente com falback para localhost.
    """
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", 6379))
    db = int(os.getenv("REDIS_DB", 0))

    return redis.Redis(
        host=host,
        port=port,
        db=db,
        decode_responses=True,  # Importante: retorna str em vez de bytes
        socket_connect_timeout=2,
        socket_timeout=2,
    )
