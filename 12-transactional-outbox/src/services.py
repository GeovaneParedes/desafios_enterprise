import json
from sqlalchemy.orm import Session
from src.models import Order, OutboxEvent


class OrderService:
    def __init__(self, session: Session):
        self.session = session

    def create_order(self, product: str, amount: int) -> int:
        """
        Cria um pedido e agenda o evento de notificação atomicamente.
        """
        # 1. Operação de Negócio
        new_order = Order(product=product, amount=amount)
        self.session.add(new_order)

        # O flush gera o ID do pedido antes do commit final,
        # mas ainda na transação
        self.session.flush()

        # 2. Criação do Evento (Outbox Pattern)
        # Salvamos a intenção de publicar, não publicamos ainda.
        event_payload = json.dumps({
            "order_id": new_order.id,
            "product": new_order.product,
            "status": "CREATED"
        })

        outbox_event = OutboxEvent(
            aggregate_id=new_order.id,
            topic="order.events",
            payload=event_payload
        )
        self.session.add(outbox_event)

        # 3. Commit Único (Atomicidade)
        # Se falhar aqui, nem o pedido nem o evento são salvos.
        self.session.commit()

        return new_order.id
