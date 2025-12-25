import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

import src.auditor  # # noqa: F401 Ativa o event listener!
from src.core import Base

# Importar models e o auditor para registrar o evento
from src.models import AuditLog, BankAccount


@pytest.fixture
def session():
    # SQLite em memória
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    # --- A MUDANÇA ESTÁ AQUI ---
    # expire_on_commit=False impede que o objeto perca os dados após o commit.
    # Isso permite que o histórico (old_values) funcione corretamente no teste
    # quando reutilizamos o mesmo objeto 'acc'.
    Session = sessionmaker(bind=engine, expire_on_commit=False)

    session = Session()
    yield session
    session.close()


def test_audit_log_flow(session):
    # 1. INSERT
    print("\n--- [Passo 1] Criando Conta (Gera Log INSERT) ---")
    acc = BankAccount(owner_name="Audit Corp", balance=1000.0)
    session.add(acc)
    session.commit()  # Dispara o before_flush

    # Verifica se gerou log de Insert
    logs = session.scalars(select(AuditLog)).all()
    assert len(logs) == 1
    assert logs[0].action == "INSERT"
    assert logs[0].new_values["balance"] == 1000.0
    print(f"✅ Log INSERT detectado: {logs[0].new_values}")

    # 2. UPDATE (Alterando Saldo)
    print("--- [Passo 2] Alterando Saldo (Gera Log UPDATE) ---")

    # Nota: Em um app real (FastAPI), você faria um 'get' antes do update,
    # o que carregaria o valor antigo (1000.0) na memória.
    # Com expire_on_commit=False, simulamos esse comportamento.
    acc.balance = 2500.0
    session.commit()

    # Busca o último log
    log = session.scalars(
        select(AuditLog).where(AuditLog.action == "UPDATE")
    ).one()

    # Agora o old_values["balance"] deve ser 1000.0, não None
    print(f"DEBUG: Old={log.old_values} New={log.new_values}")

    assert log.old_values["balance"] == 1000.0
    assert log.new_values["balance"] == 2500.0
    print(f"✅ Log UPDATE detectado: {log.old_values} -> {log.new_values}")

    # 3. SOFT DELETE (Deve gerar um UPDATE no campo is_deleted)
    print("--- [Passo 3] Soft Delete (Gera Log UPDATE) ---")
    acc.soft_delete(session)
    session.commit()

    # O Soft Delete é tecnicamente um UPDATE no banco
    logs_update = session.scalars(
        select(AuditLog).where(AuditLog.action == "UPDATE")
    ).all()

    # O último log deve ser o do soft delete
    last_log = logs_update[-1]

    assert last_log.new_values["is_deleted"] is True
    # Verifica se serializou a data corretamente (não deu erro de JSON)
    assert last_log.new_values["deleted_at"] is not None
    print(
        f"✅ Log Soft Delete detectado como alteração: {last_log.new_values}"
    )
