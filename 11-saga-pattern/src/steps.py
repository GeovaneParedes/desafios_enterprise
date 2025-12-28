from typing import Any, Dict

from loguru import logger

from src.interface import SagaStep


class StockStep(SagaStep):
    name = "StockService"

    def execute(self, context: Dict[str, Any]) -> bool:
        item = context.get("item")
        logger.info(f"📦 [Stock] Tentando reservar item: {item}...")

        # Simulação de regra de negócio
        if item == "INDISPONIVEL":
            logger.error("❌ [Stock] Falha: Item fora de estoque.")
            return False

        logger.success(f"✅ [Stock] Item {item} reservado com sucesso.")
        return True

    def compensate(self, context: Dict[str, Any]):
        item = context.get("item")
        logger.warning(
            f"↩️ [Stock] Compensação: Devolvendo {item} ao estoque...")


class PaymentStep(SagaStep):
    name = "PaymentService"

    def execute(self, context: Dict[str, Any]) -> bool:
        amount = context.get("amount")
        logger.info(f"💰 [Payment] Tentando cobrar ${amount}...")

        # Simulação de falha
        if amount > 1000:
            logger.error(
                f"❌ [Payment] Falha: Saldo insuficiente para ${amount}.")
            return False

        logger.success(f"✅ [Payment] Cobrança de ${amount} realizada.")
        return True

    def compensate(self, context: Dict[str, Any]):
        amount = context.get("amount")
        logger.warning(
            f"↩️ [Payment] Compensação: Reembolsando ${amount} ao cliente...")


class ShippingStep(SagaStep):
    name = "ShippingService"

    def execute(self, context: Dict[str, Any]) -> bool:
        logger.info("🚚 [Shipping] Gerando etiqueta de envio...")
        logger.success("✅ [Shipping] Etiqueta gerada.")
        return True

    def compensate(self, context: Dict[str, Any]):
        logger.warning(
            "↩️ [Shipping] Compensação: Cancelando etiqueta de envio...")
