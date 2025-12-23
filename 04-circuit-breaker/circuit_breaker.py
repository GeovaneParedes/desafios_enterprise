import logging
import time
from functools import wraps

import redis
from fastapi import HTTPException

# Configuração de Logs
logger = logging.getLogger("CircuitBreaker")
logging.basicConfig(level=logging.INFO)


class CircuitBreakerOpenException(Exception):
    """Exceção levantada quando o circuito está ABERTO."""

    pass


class CircuitBreaker:
    def __init__(
        self,
        redis_client: redis.Redis,
        service_name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 10,
    ):
        """
        :param redis_client: Conexão com o Redis
        :param service_name: Nome do serviço protegido (ex: 'serasa_api')
        :param failure_threshold: Quantas falhas seguidas
        abrem o circuito (ex: 5)
        :param recovery_timeout: Quanto tempo (segundos) fica aberto antes de
        tentar de novo (ex: 30s)
        """
        self.redis = redis_client
        self.name = service_name
        self.threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        # Chaves no Redis
        self.key_failures = f"cb:{service_name}:failures"
        self.key_state_open = f"cb:{service_name}:open"

    async def call(self, func, *args, **kwargs):
        """
        Executa a função protegida pelo Circuit Breaker.
        """
        # 1. Verifica se o circuito está ABERTO (OPEN)
        if self._is_open():
            logger.warning(
                f"🛡️ Circuito ABERTO para {self.name}."
                f"Rejeitando requisição (Fail Fast)."
            )
            raise CircuitBreakerOpenException(
                f"Serviço {self.name} indisponível temporariamente."
            )

        # 2. Tenta executar a função (Estado CLOSED ou HALF-OPEN)
        try:
            result = await func(*args, **kwargs)

            # SUCESSO: Se passou, reseta as falhas
            # (Fecha o circuito se estava Half-Open)
            self._reset_failures()
            return result

        except Exception as e:
            # FALHA: Registra o erro
            self._record_failure()
            logger.error(f"❌ Falha na chamada para {self.name}: {str(e)}")
            raise e

    def _is_open(self):
        """Verifica se existe a chave de bloqueio no Redis."""
        return self.redis.exists(self.key_state_open)

    def _record_failure(self):
        """Incrementa contagem de falhas.
        Se atingir limite, ABRE o circuito."""
        failures = self.redis.incr(self.key_failures)
        logger.info(
            f"⚠️ Falha registrada para {self.name}."
            f"Total: {failures}/{self.threshold}"
        )

        if failures >= self.threshold:
            self._open_circuit()

    def _open_circuit(self):
        """Abre o circuito: Cria chave com TTL no Redis."""
        logger.critical(
            f"🔥 LIMIT AÇO! Abrindo circuito para {self.name}"
            f"por {self.recovery_timeout}s."
        )
        # Define a chave 'open' com expiração (TTL)
        self.redis.setex(self.key_state_open, self.recovery_timeout, "true")

    def _reset_failures(self):
        """Sucesso! Zera contador de falhas."""
        # Só deleta se existir, para economizar operações
        if self.redis.get(self.key_failures):
            self.redis.delete(self.key_failures)
            logger.info(f"✅ Sucesso! Falhas resetadas para {self.name}.")
