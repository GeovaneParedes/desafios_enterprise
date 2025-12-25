from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    Representa um usuário do sistema.
    Esta tabela existirá duplicada em TODOS os shards, mas
    os dados serão divididos baseados no 'tenant_id'.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id},tenant={self.tenant_id},name={self.name})>"
