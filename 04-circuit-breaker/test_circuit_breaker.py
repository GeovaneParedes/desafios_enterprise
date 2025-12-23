import asyncio

import pytest
import redis

from circuit_breaker import CircuitBreaker, CircuitBreakerOpenException

# Configuração do Redis (Usa o mesmo container que já está rodando)
redis_client = redis.Redis(
    host="localhost", port=6379, db=0, decode_responses=True
)


@pytest.fixture(autouse=True)
def clean_redis():
    """Limpa o Redis antes de cada teste para garantir isolamento"""
    redis_client.flushall()
    yield


# --- Funções Simuladas (Mocks) ---
async def funcao_sucesso():
    return "DADOS_VALIDOS"


async def funcao_falha():
    raise Exception("Erro de Conexão Simulado")


# --- Testes ---


@pytest.mark.asyncio
async def test_circuit_state_closed_initially():
    """O circuito deve começar FECHADO e permitir chamadas."""
    cb = CircuitBreaker(
        redis_client, "test_service", failure_threshold=2, recovery_timeout=1
    )
    resultado = await cb.call(funcao_sucesso)
    assert resultado == "DADOS_VALIDOS"
    assert cb._is_open() == 0  # 0 keys exist


@pytest.mark.asyncio
async def test_circuit_opens_after_failures():
    """O circuito deve ABRIR após atingir o limite de falhas."""
    # Configura limite baixo (2 falhas)
    cb = CircuitBreaker(
        redis_client, "test_service", failure_threshold=2, recovery_timeout=5
    )

    # 1. Primeira Falha
    with pytest.raises(Exception):
        await cb.call(funcao_falha)

    # 2. Segunda Falha (Atingiu o limite)
    with pytest.raises(Exception):
        await cb.call(funcao_falha)

    # 3. Terceira tentativa: Deve ser BLOQUEADA pelo Circuit Breaker (Fail Fast)
    # Note que esperamos CircuitBreakerOpenException, não a Exception genérica da função
    with pytest.raises(CircuitBreakerOpenException):
        await cb.call(funcao_falha)

    assert cb._is_open() == 1  # Chave deve existir no Redis


@pytest.mark.asyncio
async def test_circuit_recovery_half_open():
    """O circuito deve tentar se recuperar após o timeout (Half-Open)."""
    # Timeout bem curto (1 segundo) para o teste ser rápido
    cb = CircuitBreaker(
        redis_client, "test_service", failure_threshold=1, recovery_timeout=1
    )

    # 1. Força a falha e abre o circuito
    with pytest.raises(Exception):
        await cb.call(funcao_falha)

    # Valida que está aberto
    with pytest.raises(CircuitBreakerOpenException):
        await cb.call(funcao_sucesso)

    # 2. Espera o TTL do Redis expirar (1.1s)
    await asyncio.sleep(1.2)

    # 3. Tenta de novo (Estado Half-Open -> Closed)
    # Agora deve passar porque a função é de sucesso
    resultado = await cb.call(funcao_sucesso)
    assert resultado == "DADOS_VALIDOS"

    # Verifica se as falhas foram zeradas
    assert redis_client.get(cb.key_failures) is None
