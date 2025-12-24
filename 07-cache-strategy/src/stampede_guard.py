import logging
from typing import Any, Callable

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
        self, key: str, ttl_seconds: int, computer: Callable[[], Any]
    ) -> Any:
        """
        Recupera valor do cache ou computa se não existir, garantindo que
        apenas
        UMA thread execute a computação (computer) simultaneamente.

        Args:
            key: Chave do cache.
            ttl_seconds: Tempo de vida do cache em segundos.
            computer: Função lambda/callback que busca o dado na fonte real
            (DB/API) se der Cache Miss.

        Returns:
        O valor do dado (str ou bytes, dependendo da decodificação do Redis).
        """
        # 1. Tentativa Otimista: Leitura direta (Caminho feliz)
        value = self.redis.get(key)
        if value:
            logger.debug(f"Cache HIT inicial: {key}")
            return value

        # 2. Cache Miss: Inicia protocolo de proteção
        logger.info(f"Cache MISS: {key}. Iniciando protocolo de lock.")
        return self._fetch_with_lock(key, ttl_seconds, computer)

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=0.1, min=0.1, max=1.0),
        retry=retry_if_exception_type(
            BlockingIOError
        ),  # Custom exception para forçar retry
    )
    def _fetch_with_lock(
        self, key: str, ttl: int, computer: Callable[[], Any]
    ) -> Any:
        """
        Tenta adquirir lock distribuído. Se falhar, aguarda e tenta ler do
        cache novamente.
        """
        lock_key = f"lock:{key}"

        # Tenta adquirir o lock (Mutex) - Expira em 5s para evitar deadlock se
        # o processo morrer
        lock = self.redis.lock(lock_key, timeout=5, blocking=False)

        acquired = lock.acquire()

        if not acquired:
            # Se não conseguiu o lock, significa que alguém já está computando.
            # Verificamos o cache novamente antes de desistir (pode ter ficado
            # pronto agora).
            value = self.redis.get(key)
            if value:
                logger.info(f"Cache HIT durante espera do lock: {key}")
                return value

            # Se ainda não está no cache e não peguei o lock, lança erro para
            # o Tenacity tentar de novo
            logger.debug("Lock ocupado. Aguardando backoff...")
            raise BlockingIOError("Lock is busy")

        try:
            # --- ZONA CRÍTICA ---

            # 3. Double-Checked Locking (Crucial!)
            # Verifica se, entre o MISS inicial e a aquisição do Lock, alguém
            # preencheu o cache.
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
                pass  # Lock pode ter expirado ou já liberado
