import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Order(Base):
    """Tabela de Negócio"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class OutboxEvent(Base):
    """
    Tabela de Outbox.
    Armazena eventos que DEVEM ser publicados, garantindo atomicidade com a regra de negócio.
    """
    __tablename__ = "outbox_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    aggregate_id = Column(Integer, nullable=False) # ID do Pedido
    topic = Column(String, nullable=False)         # Ex: "order.created"
    payload = Column(Text, nullable=False)         # JSON do evento
    
    # Controle de processamento
    processed = Column(Boolean, default=False)
    processed_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<OutboxEvent {self.id} | {self.topic} | Processed: {self.processed}>"
