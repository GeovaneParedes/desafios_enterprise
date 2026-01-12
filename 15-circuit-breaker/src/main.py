import time
from loguru import logger
from src.circuit import CircuitBreaker, CircuitBreakerOpenException
from src.service import UnstableService


def run_simulation():
    # Config: Abre após 3 falhas. Tenta recuperar após 3 segundos.
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=3)
    service = UnstableService()

    logger.info("🟢 --- FASE 1: Tudo funcionando ---")
    for i in range(3):
        try:
            res = cb.call(service.process_payment, 100)
            logger.info(f"Req {i+1}: {res}")
        except Exception as e:
            logger.error(f"Req {i+1}: {e}")
        time.sleep(0.5)

    logger.info("\n🔴 --- FASE 2: O Serviço cai! ---")
    service.should_fail = True

    # Vamos fazer 5 chamadas.
    # As 3 primeiras vão falhar "de verdade" (ConnectionError).
    # A 4ª e 5ª vão falhar rápido (CircuitBreakerOpenException).
    for i in range(5):
        try:
            cb.call(service.process_payment, 100)
        except CircuitBreakerOpenException as e:
            logger.warning(f"🛡️ Bloqueado pelo Circuito: {e}")
        except Exception as e:
            logger.error(f"💥 Erro da API: {e}")
        time.sleep(0.5)

    logger.info("\n⏳ --- FASE 3: Esperando Recuperação (3s) ---")
    time.sleep(3.5)

    logger.info("\n🟡 --- FASE 4: Tentativa de Recuperação (Half-Open) ---")
    # Serviço volta ao ar
    service.should_fail = False

    # A primeira chamada será o teste (Half-Open). Se passar, reseta.
    for i in range(3):
        try:
            res = cb.call(service.process_payment, 100)
            logger.info(f"Req Pós-Recuperação {i+1}: {res}")
        except Exception as e:
            logger.error(f"Erro: {e}")
        time.sleep(0.5)


if __name__ == "__main__":
    run_simulation()
