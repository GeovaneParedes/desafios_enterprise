from typing import Any, Dict, List

from loguru import logger

from src.interface import SagaStep


class SagaOrchestrator:
    def __init__(self):
        self.steps: List[SagaStep] = []

    def add_step(self, step: SagaStep):
        self.steps.append(step)

    def run(self, context: Dict[str, Any]) -> bool:
        logger.info("🎬 Iniciando Saga Transacional...")
        executed_steps: List[SagaStep] = []
        success = True

        # 1. Fase de Execução (Ida)
        for step in self.steps:
            result = step.execute(context)

            if result:
                executed_steps.append(step)
            else:
                success = False
                logger.error(f"⛔ Falha no passo {step.name}."
                             f"Iniciando Rollback...")
                break

        # 2. Se tudo deu certo, fim.
        if success:
            logger.info("✨ Saga completada com sucesso!")
            return True

        # 3. Fase de Compensação (Volta) - Apenas para os que executaram com
        # sucesso
        # Percorre a lista de trás para frente (LIFO)
        for step in reversed(executed_steps):
            step.compensate(context)

        logger.info("🏁 Rollback finalizado. Sistema consistente.")
        return False
