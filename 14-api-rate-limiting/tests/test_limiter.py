import time

import pytest
import redis  # noqa

from src.limiter import RateLimiter


@pytest.fixture(scope="module")
def redis_client():
    # Setup: Conecta e limpa o banco
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    r.flushdb()
    yield r
    r.flushdb()  # Teardown


def test_rate_limit_enforcement(redis_client):
    """Verifica se bloqueia após exceder o limite."""
    limit = 3
    window = 2
    limiter = RateLimiter(redis_client, limit, window)
    user = "test_user_1"

    # 3 Requisições permitidas
    assert limiter.is_allowed(user) is True
    assert limiter.is_allowed(user) is True
    assert limiter.is_allowed(user) is True

    # A 4ª deve ser bloqueada
    assert limiter.is_allowed(user) is False


def test_rate_limit_window_reset(redis_client):
    """Verifica se libera após o tempo passar."""
    limit = 1
    window = 2
    limiter = RateLimiter(redis_client, limit, window)
    user = "test_user_2"

    # 1ª Permitida
    assert limiter.is_allowed(user) is True

    # 2ª Bloqueada (Imediato)
    assert limiter.is_allowed(user) is False

    # Espera a janela passar
    time.sleep(window + 0.1)

    # Deve permitir novamente
    assert limiter.is_allowed(user) is True
