import time
from concurrent.futures import ThreadPoolExecutor

import pytest
import redis

from src.stampede_guard import CacheStampedeProtector


# Setup do Redis (Assumindo Docker rodando)
@pytest.fixture
def redis_client():
    client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    client.flushall()  # Limpa banco antes do teste
    yield client
    client.close()


def test_stampede_protection(redis_client):
    """
    Simula 50 threads tentando acessar o mesmo recurso simultaneamente.
    O contador de acesso ao 'banco de dados' deve ser 1.
    """
    protector = CacheStampedeProtector(redis_client)
    key = "user:profile:123"

    # Variável compartilhada para contar acessos reais (simula DB)
    # Em um cenário real, isso seria um mock ou spy
    execution_counter = {"count": 0}

    def expensive_database_call():
        # Simula latência de I/O
        time.sleep(0.1)
        execution_counter["count"] += 1
        return "dados_do_usuario_json"

    def worker_task():
        return protector.get_or_compute(key, 60, expensive_database_call)

    # Dispara 50 threads simultâneas
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(lambda _: worker_task(), range(50)))

    # Assertions
    # 1. Todas as threads devem receber o valor correto
    assert all(r == "dados_do_usuario_json" for r in results)

    # 2. A computação pesada deve ter ocorrido APENAS UMA VEZ
    # Se fosse sem proteção, esse número seria próximo de 50
    assert execution_counter["count"] == 1

    # 3. Verificar se o valor está no Redis
    assert redis_client.get(key) == "dados_do_usuario_json"
