from src.orchestrator import SagaOrchestrator
from src.steps import PaymentStep, ShippingStep, StockStep


def run_success_scenario():
    print("\n--- CENÁRIO 1: Compra Bem Sucedida ---")
    saga = SagaOrchestrator()
    saga.add_step(StockStep())
    saga.add_step(PaymentStep())
    saga.add_step(ShippingStep())

    # Item normal, Valor baixo
    context = {"item": "Notebook", "amount": 500}
    saga.run(context)


def run_failure_scenario():
    print("\n--- CENÁRIO 2: Falha no Pagamento (Deve disparar Rollback) ---")
    saga = SagaOrchestrator()
    saga.add_step(StockStep())
    saga.add_step(PaymentStep())
    saga.add_step(ShippingStep())

    # Valor alto força falha no PaymentStep
    context = {"item": "Gamer PC", "amount": 9999}
    saga.run(context)


if __name__ == "__main__":
    run_success_scenario()
    run_failure_scenario()
