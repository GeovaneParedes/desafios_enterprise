import pytest
import time
from src.circuit import CircuitBreaker, State, CircuitBreakerOpenException


def successful_func():
    return "ok"


def failing_func():
    raise ValueError("error")


class TestCircuitBreaker:

    def test_initial_state_closed(self):
        cb = CircuitBreaker()
        assert cb.state == State.CLOSED
        assert cb.call(successful_func) == "ok"

    def test_opens_after_threshold(self):
        cb = CircuitBreaker(failure_threshold=2)

        # 1ª Falha
        with pytest.raises(ValueError):
            cb.call(failing_func)
        assert cb.state == State.CLOSED

        # 2ª Falha -> Deve Abrir
        with pytest.raises(ValueError):
            cb.call(failing_func)
        assert cb.state == State.OPEN

    def test_fail_fast_when_open(self):
        cb = CircuitBreaker(failure_threshold=1)

        # Força abertura
        with pytest.raises(ValueError):
            cb.call(failing_func)

        # Agora deve lançar CircuitBreakerOpenException imediatamente
        # sem nem tentar chamar a função (mock)
        with pytest.raises(CircuitBreakerOpenException):
            cb.call(failing_func)

    def test_half_open_recovery(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.1)

        # Abre
        with pytest.raises(ValueError):
            cb.call(failing_func)
        assert cb.state == State.OPEN

        # Espera timeout
        time.sleep(0.2)

        # Próxima chamada muda para HALF_OPEN internamente e tenta
        # Se sucesso -> CLOSED
        assert cb.call(successful_func) == "ok"
        assert cb.state == State.CLOSED
        assert cb.failure_count == 0
