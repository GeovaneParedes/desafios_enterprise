import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from src.models import Base, Order, OutboxEvent
from src.services import OrderService
from src.relay import OutboxRelay, FakeMessageBroker

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_atomic_creation(session):
    """Prova que criar pedido gera evento na mesma transação."""
    service = OrderService(session)
    service.create_order("Mouse", 50)

    # Verifica Pedido
    orders = session.scalars(select(Order)).all()
    assert len(orders) == 1
    
    # Verifica Outbox
    events = session.scalars(select(OutboxEvent)).all()
    assert len(events) == 1
    assert events[0].aggregate_id == orders[0].id
    assert events[0].processed is False

def test_relay_publish_success(session):
    """Prova que o relay processa e marca como feito."""
    # Setup
    service = OrderService(session)
    service.create_order("Teclado", 100)
    
    # Mock do Broker para garantir sucesso
    mock_broker = MagicMock()
    mock_broker.publish.return_value = True
    
    # Executa Relay
    relay = OutboxRelay(session, mock_broker)
    relay.process_outbox()

    # Verifica DB
    event = session.scalar(select(OutboxEvent))
    assert event.processed is True
    assert event.processed_at is not None
    mock_broker.publish.assert_called_once()

def test_relay_broker_failure_retry(session):
    """Prova que se o broker falha, o evento NÃO é marcado como processado (será tentado dnv)."""
    service = OrderService(session)
    service.create_order("Monitor", 2000)

    # Mock do Broker falhando (lançando exceção)
    mock_broker = MagicMock()
    mock_broker.publish.side_effect = Exception("Kafka fora do ar!")

    relay = OutboxRelay(session, mock_broker)
    relay.process_outbox() # Vai logar erro, mas não deve crashar o worker

    # Verifica DB: O evento deve continuar processed=False
    event = session.scalar(select(OutboxEvent))
    assert event.processed is False
    assert event.processed_at is None
