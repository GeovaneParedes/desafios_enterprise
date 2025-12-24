import fakeredis
import pytest

from src.stampede_guard import CacheStampedeProtector


@pytest.fixture
def fake_redis():
    """
    Cria um redis falso na memória.
    IMPORTANTE: 'version=7' habilita suporte a comandos LUA (evalsha)
    que a biblioteca redis-py usa para gerenciar Locks.
    """
    # Instancia diretamente com a versão 7 explícita
    client = fakeredis.FakeRedis(version="7", decode_responses=True)
    yield client
    client.flushall()


def test_cache_miss_computes_value(fake_redis):
    """Testa se o valor é computado quando não existe no cache."""
    protector = CacheStampedeProtector(fake_redis)
    key = "unit:test:key"
    expected_value = "computed_data"

    # Função que simula cálculo
    call_count = 0

    def computer():
        nonlocal call_count
        call_count += 1
        return expected_value

    # Executa
    result = protector.get_or_compute(key, 60, computer)

    # Asserts
    assert result == expected_value
    assert call_count == 1
    assert fake_redis.get(key) == expected_value


def test_cache_hit_skips_computation(fake_redis):
    """Testa se a computação é evitada quando valor já existe."""
    protector = CacheStampedeProtector(fake_redis)
    key = "unit:test:existing"
    fake_redis.set(key, "cached_data")

    def computer():
        raise Exception("Não deveria ser chamado!")

    result = protector.get_or_compute(key, 60, computer)
    assert result == "cached_data"
