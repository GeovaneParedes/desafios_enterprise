from unittest.mock import MagicMock


from src.orchestrator import SagaOrchestrator
from src.steps import PaymentStep, ShippingStep, StockStep


class TestSagaOrchestrator:

    def test_full_success_flow(self):
        """
        Valida se todos os passos são executados em ordem quando não há erros.
        """
        # Arrange
        context = {"item": "Mouse", "amount": 50}
        saga = SagaOrchestrator()

        # Mocks para verificar chamadas
        step1 = StockStep()
        step1.execute = MagicMock(wraps=step1.execute)
        step1.compensate = MagicMock(wraps=step1.compensate)

        step2 = PaymentStep()
        step2.execute = MagicMock(wraps=step2.execute)
        step2.compensate = MagicMock(wraps=step2.compensate)

        saga.add_step(step1)
        saga.add_step(step2)

        # Act
        result = saga.run(context)

        # Assert
        assert result is True
        # Ambos executaram
        step1.execute.assert_called_once()
        step2.execute.assert_called_once()
        # Ninguém compensou
        step1.compensate.assert_not_called()
        step2.compensate.assert_not_called()

    def test_rollback_flow(self):
        """
        Valida se a compensação é acionada apenas para os passos concluídos
        antes da falha.
        """
        # Arrange
        # Valor 5000 força falha no PaymentStep
        context = {"item": "MacBook", "amount": 5000}
        saga = SagaOrchestrator()

        step1 = StockStep()  # Vai passar
        step1.execute = MagicMock(wraps=step1.execute)
        step1.compensate = MagicMock(wraps=step1.compensate)

        step2 = PaymentStep()  # Vai falhar
        step2.execute = MagicMock(wraps=step2.execute)
        step2.compensate = MagicMock(wraps=step2.compensate)

        step3 = ShippingStep()  # Nem deve ser chamado
        step3.execute = MagicMock(wraps=step3.execute)
        step3.compensate = MagicMock(wraps=step3.compensate)

        saga.add_step(step1)
        saga.add_step(step2)
        saga.add_step(step3)

        # Act
        result = saga.run(context)

        # Assert
        assert result is False

        # Step 1 (Stock): Executou e Compensou (Rollback)
        step1.execute.assert_called_once()
        step1.compensate.assert_called_once()

        # Step 2 (Payment): Executou, Falhou, NÃO deve compensar (pois falhou)
        step2.execute.assert_called_once()
        step2.compensate.assert_not_called()

        # Step 3 (Shipping): Não deve ter feito nada
        step3.execute.assert_not_called()
        step3.compensate.assert_not_called()
