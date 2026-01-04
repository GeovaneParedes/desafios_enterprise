import time
import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models import OutboxEvent


class FakeMessageBroker:
    """Simula um Kafka/RabbitMQ que pode falhar aleatoriamente."""

    def publish(self, topic: str, message: str):
        # Simulando latência de rede
        print(f"📡 [Broker] Publicando no tópico '{topic}': {message}")
        return True


class OutboxRelay:
    def __init__(self, session: Session, broker: FakeMessageBroker):
        self.session = session
        self.broker = broker

    def process_outbox(self):
        """
        Lê eventos pendentes e os publica.
        """
        # 1. Busca eventos não processados
        events = self.session.scalars(
            select(OutboxEvent)
            .where(OutboxEvent.processed == False)
            .order_by(OutboxEvent.created_at)
        ).all()

        if not events:
            print("💤 [Relay] Nada para processar.")
            return

        print(f"⚙️ [Relay] Encontrados {len(events)} eventos pendentes.")

        for event in events:
            try:
                # 2. Tenta publicar no Broker (Ponto de falha externa)
                success = self.broker.publish(event.topic, event.payload)

                if success:
                    # 3. Marca como processado APÓS confirmação do broker
                    # (At-Least-Once Delivery)
                    event.processed = True
                    event.processed_at = datetime.datetime.utcnow()
                    print(
                       f"✅ [Relay] Evento {event.id} processado com sucesso.")

            except Exception as e:
                print(f"❌ [Relay] Falha ao publicar evento {event.id}: {e}")
                # Em um sistema real, implementaríamos Retry Backoff
                # aqui ou DLQ

        # 4. Salva o estado atualizado dos eventos
        self.session.commit()
