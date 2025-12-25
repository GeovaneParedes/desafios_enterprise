import logging
from typing import Any, Callable, Optional

import redis
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LockAcquisitionError(Exception):
    """
    Exceção personalizada lançada quando não é possível adquirir o lock.
    Sinaliza para o Tenacity que devemos tentar novamente (Backoff).
    """

    pass


class CacheStampedeProtector:
    """
    Gerenciador de Cache com proteção contra Thundering Herd (Cache Stampede).
    Utiliza Distributed Locking e Double-Checked Locking.
    """

    def __init__(self, redis_client: redis.Redis):
        """
        Inicializa o protetor.

        Args:
            redis_client: Instância conectada do cliente Redis.
        """
        self.redis = redis_client

    def get_or_compute(
        self,
        key: str,
        ttl_seconds: int,
        computer: Callable[[], Any],
        lock_timeout: int = 5,
    ) -> Any:
        """
        Recupera valor do cache ou computa se não existir, garantindo que
        apenas UMA thread execute a computação simultaneamente.

        Args:
            key: Chave do cache.
            ttl_seconds: Tempo de vida do cache em segundos.
            computer: Função lambda/callback que busca o dado na fonte real.
            lock_timeout: Tempo máximo (em segundos) que o lock pode ser
                          segurado. Deve ser maior que o tempo esperado da
                          computação para evitar que o lock expire no meio.

        Returns:
            O valor do dado.
        """
        # 1. Tentativa Otimista: Leitura direta (Caminho feliz)
        value = self.redis.get(key)
        if value:
            logger.debug(f"Cache HIT inicial: {key}")
            return value

        # 2. Cache Miss: Inicia protocolo de proteção
        logger.info(f"Cache MISS: {key}. Iniciando protocolo de lock.")
        return self._fetch_with_lock(key, ttl_seconds, computer, lock_timeout)

    @retry(
        stop=stop_after_attempt(
            10
        ),  # Aumentei para 10 tentativas (mais robusto)
        wait=wait_exponential(multiplier=0.1, min=0.1, max=2.0),
        retry=retry_if_exception_type(LockAcquisitionError),
        reraise=True,  # Se falhar 10x, lança o erro original
    )
    def _fetch_with_lock(
        self,
        key: str,
        ttl: int,
        computer: Callable[[], Any],
        lock_timeout: int,
    ) -> Any:
        """
        Tenta adquirir lock distribuído. Se falhar, aguarda e tenta ler do
        cache novamente.
        """
        lock_key = f"lock:{key}"

        # Tenta adquirir o lock (Mutex) - Usa o timeout configurável
        lock = self.redis.lock(lock_key, timeout=lock_timeout, blocking=False)
        acquired = lock.acquire()

        if not acquired:
            # Se não conseguiu o lock, significa que alguém já está computando.
            # Verificamos o cache novamente antes de desistir.
            value = self.redis.get(key)
            if value:
                logger.info(f"Cache HIT durante espera do lock: {key}")
                return value

            # Lança nossa exceção personalizada para acionar o retry
            logger.debug("Lock ocupado. Aguardando backoff...")
            raise LockAcquisitionError("Lock is busy")

        try:
            # --- ZONA CRÍTICA ---

            # 3. Double-Checked Locking (Crucial!)
            value = self.redis.get(key)
            if value:
                logger.info(
                    f"Cache HIT dentro da Zona Crítica (Double-Check): {key}"
                )
                return value

            # 4. Computação Real (Acesso ao DB/API lento)
            logger.info(f"Executando computação pesada para: {key}")
            computed_value = computer()

            # 5. Atualização do Cache
            self.redis.setex(key, ttl, computed_value)
            return computed_value

        finally:
            # Libera o lock de forma segura
            try:
                lock.release()
            except redis.exceptions.LockError:
                # Lock pode ter expirado (se a computação demorou mais que
                # lock_timeout) ou já liberado. Apenas logamos warning.
                logger.warning(
                    f"Tentativa de liberar lock expirado"
                    f"ou inexistente: {lock_key}"
                )
