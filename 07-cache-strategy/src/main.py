import logging
import os
import random
import sys
import time

# Ajuste para garantir que o python encontre os módulos no diretório atual
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cache_client import get_redis_client
from stampede_guard import CacheStampedeProtector, LockAcquisitionError

# Configuração de Logs para ver o fluxo no terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("DemoApp")


def fake_expensive_query():
    """
    Simula uma consulta pesada ao banco de dados ou API externa.
    Demora entre 2 a 3 segundos.
    """
    logger.warning("🐢 Iniciando consulta pesada ao Banco de Dados...")
    time.sleep(2)  # Simula latência
    result = f"Dados do Relatório #{random.randint(1000, 9999)}"
    logger.warning(f"✅ Consulta finalizada! Resultado: {result}")
    return result


def main():
    logger.info("--- 🚀 Iniciando Demo: Cache Stampede Protection ---")

    # 1. Setup
    try:
        redis = get_redis_client()
        redis.ping()  # Teste de conexão
    except Exception as e:
        logger.error(f"❌ Erro ao conectar no Redis: {e}")
        logger.error(
            "Verifique se o container docker está rodando"
            "(docker-compose up -d)"
        )
        return

    protector = CacheStampedeProtector(redis)
    key = "dashboard:relatorio_financeiro"
    ttl = 10  # TTL curto para facilitar testes

    # Limpa a chave para garantir o teste do 'Cold Start'
    redis.delete(key)
    logger.info(f"🧹 Chave '{key}' limpa para o teste.")

    # 2. Primeira Chamada (Cold Start)
    # Aqui o cache está vazio. Deve pegar o Lock, ir no "Banco" e salvar.
    logger.info("\n➡️  Tentativa 1: Cache Vazio (Deve demorar ~2s)")
    start = time.time()

    val1 = protector.get_or_compute(
        key=key, ttl_seconds=ttl, computer=fake_expensive_query
    )

    duration = time.time() - start
    logger.info(f"📦 Valor recebido: {val1}")
    logger.info(f"⏱️  Tempo total: {duration:.4f}s (Esperado: > 2s)")

    # 3. Segunda Chamada (Warm Start)
    # Aqui o dado já está no Redis. Deve ser instantâneo.
    logger.info("\n➡️  Tentativa 2: Cache Quente (Deve ser instantâneo)")
    start = time.time()

    val2 = protector.get_or_compute(
        key=key, ttl_seconds=ttl, computer=fake_expensive_query
    )

    duration = time.time() - start
    logger.info(f"📦 Valor recebido: {val2}")
    logger.info(f"⏱️  Tempo total: {duration:.4f}s (Esperado: < 0.01s)")

    logger.info("\n--- 🎉 Demo Finalizada com Sucesso ---")


if __name__ == "__main__":
    main()
