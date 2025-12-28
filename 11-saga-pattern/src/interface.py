from abc import ABC, abstractmethod
from typing import Any, Dict


class SagaStep(ABC):
    """
    Interface que define um passo dentro de uma transação distribuída (Saga).
    Todo passo deve ter uma ação (execute) e uma reação de desfazimento
    (compensate).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Realiza a operação de negócio.
        Retorna True se sucesso, False se falha.
        O 'context' é usado para passar dados entre os passos.
        """
        pass

    @abstractmethod
    def compensate(self, context: Dict[str, Any]):
        """
        Desfaz a operação realizada no execute.
        Deve ser idempotente (pode ser chamado várias vezes sem efeitos
        colaterais extras).
        """
        pass
