from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Configuração do DB de Escrita (Relacional)
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    Modelo de Domínio (Write Model).
    Focado na consistência e regras de negócio.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    # Dado sensível, nunca deve ir para a leitura!


# Cria as tabelas
Base.metadata.create_all(engine)
