import random
import time

class UnstableService:
    def __init__(self):
        self.should_fail = False

    def process_payment(self, amount: float):
        """
        Simula processamento. Se should_fail for True, lança erro.
        """
        if self.should_fail:
            # Simula timeout ou erro 500
            time.sleep(0.1) 
            raise ConnectionError("Serviço de Pagamento Indisponível")
        
        return f"Pagamento de ${amount} processado."
