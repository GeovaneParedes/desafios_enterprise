import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from src.core import Base
from src.models import BankAccount


# Configuração de Teste (SQLite em memória)
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_soft_delete_flow(session):
    # 1. Criação
    print("\n--- [Passo 1] Criando Conta ---")
    account = BankAccount(owner_name="Geovane Enterprise", balance=5000.0)
    session.add(account)
    session.commit()
    account_id = account.id

    assert account_id is not None
    assert account.is_deleted is False

    # 2. Soft Delete
    print("--- [Passo 2] Executando Soft Delete ---")
    account.soft_delete(session)
    session.commit()

    # Limpa a sessão para garantir que vamos buscar do banco, não do cache
    session.expire_all()

    # 3. Busca Padrão (Deve vir VAZIO por causa do Filtro Global)
    print("--- [Passo 3] Busca Padrão (Esperando None) ---")
    stmt = select(BankAccount).where(BankAccount.id == account_id)

    # Usamos scalar_one_or_none() porque agora esperamos que não venha nada
    result = session.execute(stmt).scalar_one_or_none()

    assert (
        result is None
    ), "ERRO: O Filtro Global falhou! A conta deletada apareceu."
    print("✅ Sucesso: A conta deletada está invisível para queries normais.")

    # 4. Busca Administrativa (Ignorando o filtro)
    print("--- [Passo 4] Busca Admin (Recuperando deletado) ---")
    stmt_admin = select(BankAccount).where(BankAccount.id == account_id)

    # AQUI ESTÁ O TRUQUE: execution_options(include_deleted=True)
    stmt_admin = stmt_admin.execution_options(include_deleted=True)

    result_admin = session.execute(stmt_admin).scalar_one()

    assert result_admin is not None
    assert result_admin.is_deleted is True
    assert result_admin.deleted_at is not None
    print(f"✅ Sucesso: Conta recuperada no modo Admin: {result_admin}")
