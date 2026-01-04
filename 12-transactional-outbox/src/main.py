from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base
from src.services import OrderService
from src.relay import OutboxRelay, FakeMessageBroker

# Setup DB (SQLite em memória)
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def run_simulation():
    session = Session()
    service = OrderService(session)
    broker = FakeMessageBroker()
    relay = OutboxRelay(session, broker)

    print("--- 🛒 Passo 1: Cliente Cria Pedido (Transação DB) ---")
    order_id = service.create_order("iPhone 15", 9999)
    print(f"✅ Pedido {order_id} salvo no DB. Evento salvo na Outbox (mas não publicado ainda).")

    print("\n--- 🕵️ Passo 2: Verificando o DB antes do Relay ---")
    # Aqui o evento deve existir com processed=False
    from src.models import OutboxEvent
    from sqlalchemy import select
    event = session.scalar(select(OutboxEvent).where(OutboxEvent.aggregate_id == order_id))
    print(f"📋 Estado do Outbox: ID={event.id}, Processed={event.processed}")

    print("\n--- ⚙️ Passo 3: Executando o Outbox Relay (Worker) ---")
    relay.process_outbox()

    print("\n--- 🕵️ Passo 4: Verificando o DB pós Relay ---")
    session.refresh(event)
    print(f"📋 Estado do Outbox: ID={event.id}, Processed={event.processed}, At={event.processed_at}")

if __name__ == "__main__":
    run_simulation()
