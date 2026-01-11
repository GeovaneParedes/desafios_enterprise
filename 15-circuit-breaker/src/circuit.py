import time
from enum import Enum
from typing import Callable, Any
from loguru import logger

class State(Enum):
    CLOSED = "CLOSED"       # Tudo normal
    OPEN = "OPEN"           # Falha total, bloqueando chamadas
    HALF_OPEN = "HALF_OPEN" # Testando recuperação

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 5):
        """
        Args:
            failure_threshold: Quantas falhas seguidas abrem o circuito.
            recovery_timeout: Segundos para esperar antes de tentar de novo (Half-Open).
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        
        self.state = State.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Executa a função protegida pelo Circuit Breaker.
        """
        # 1. Se estiver ABERTO, verifica se já deu o tempo de tentar de novo
        if self.state == State.OPEN:
            elapsed = time.time() - self.last_failure_time
            if elapsed > self.recovery_timeout:
                logger.warning("⚠️ Tempo de recuperação passou. Mudando para HALF-OPEN.")
                self.state = State.HALF_OPEN
            else:
                # Falha rápida (Fail Fast)
                raise CircuitBreakerOpenException(f"Circuito ABERTO. Tente novamente em {self.recovery_timeout - elapsed:.2f}s")

        # 2. Tenta executar
        try:
            result = func(*args, **kwargs)
            
            # Se sucesso no HALF-OPEN, o sistema voltou!
            if self.state == State.HALF_OPEN:
                logger.success("✅ Recuperação confirmada! Fechando o circuito.")
                self.reset()
                
            return result

        except Exception as e:
            # Se for exceção do próprio circuito, só repassa
            if isinstance(e, CircuitBreakerOpenException):
                raise e
                
            self._handle_failure()
            raise e

    def _handle_failure(self):
        """Registra a falha e decide se abre o circuito."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        logger.error(f"❌ Falha detectada ({self.failure_count}/{self.failure_threshold})")

        if self.state == State.HALF_OPEN:
            logger.error("⛔ Falha na recuperação (Half-Open). Voltando para OPEN.")
            self.state = State.OPEN
        
        elif self.failure_count >= self.failure_threshold:
            logger.error("💥 Limite de falhas atingido! Abrindo o circuito (OPEN).")
            self.state = State.OPEN

    def reset(self):
        self.state = State.CLOSED
        self.failure_count = 0
