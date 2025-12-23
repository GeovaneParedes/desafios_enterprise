import time
import uuid
import logging
from redis import Redis

logger = logging.getLogger("DistLock")
logging.basicConfig(level=logging.INFO)

class DistributedLock:
    def __init__(self, redis_client: Redis, lock_name: str, expire_seconds: int = 5):
        """
        :param redis_client: Conexão com o Redis
        :param lock_name: Nome do recurso (ex: 'seat_1A', 'inventory_sku_123')
        :param expire_seconds: TTL de segurança para evitar Deadlock se o app travar
        """
        self.redis = redis_client
        self.lock_key = f"lock:{lock_name}"
        self.expire = expire_seconds
        self.token = str(uuid.uuid4()) # Identificador único de QUEM travou

    def acquire(self, blocking: bool = True, timeout: int = 5) -> bool:
        """
        Tenta adquirir a trava.
        Usa o comando SET resource_name my_random_value NX PX 30000
        NX = Apenas se não existir
        PX = Expira em X milissegundos
        """
        start_time = time.time()
        
        while True:
            # Tenta pegar a trava
            if self.redis.set(self.lock_key, self.token, ex=self.expire, nx=True):
                logger.info(f"🔒 Lock adquirido: {self.lock_key} (Token: {self.token})")
                return True
            
            # Se não quiser esperar (Fail Fast)
            if not blocking:
                logger.warning(f"🚫 Falha ao adquirir lock (Non-blocking): {self.lock_key}")
                return False

            # Verifica timeout de espera
            if (time.time() - start_time) > timeout:
                logger.error(f"⏰ Timeout esperando pelo lock: {self.lock_key}")
                return False

            # Backoff: Espera um pouquinho antes de tentar de novo (evita spam no Redis)
            time.sleep(0.1)

    def release(self):
        """
        Libera a trava de forma atômica usando Lua Script.
        Só libera se o token no Redis for IGUAL ao meu token.
        Isso impede que eu apague a trava de outra pessoa se a minha expirou.
        """
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        try:
            result = self.redis.eval(lua_script, 1, self.lock_key, self.token)
            if result:
                logger.info(f"🔓 Lock liberado com sucesso: {self.lock_key}")
            else:
                logger.warning(f"⚠️ Tentativa de liberar lock que não é meu ou expirou: {self.lock_key}")
        except Exception as e:
            logger.error(f"Erro ao liberar lock: {e}")

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
