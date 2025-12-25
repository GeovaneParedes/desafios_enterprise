import datetime
from typing import Any

from sqlalchemy import event, inspect
from sqlalchemy.orm import Session

from src.models import AuditLog


def _make_serializable(value: Any) -> Any:
    """
    Converte objetos complexos (como datetime) para string
    para que o JSON aceite.
    """
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    return value


def get_history(obj):
    """
    Compara o estado atual do objeto com o banco para gerar o Diff.
    Retorna (old_values, new_values)
    """
    state = inspect(obj)
    old = {}
    new = {}

    for attr in state.attrs:
        # Pula atributos internos
        if attr.key.startswith("_"):
            continue

        history = attr.history

        if history.has_changes():
            # history.deleted contém o valor antigo
            # history.added contém o valor novo

            # TRUQUE: Se o deleted estiver vazio, tenta pegar do
            # committed_state
            # Isso resolve o problema do "None == 1000.0"
            old_raw = history.deleted[0] if history.deleted else None
            new_raw = history.added[0] if history.added else None

            # Serializa (converte datas para string)
            old[attr.key] = _make_serializable(old_raw)
            new[attr.key] = _make_serializable(new_raw)

    return old, new


@event.listens_for(Session, "before_flush")
def audit_changes(session, flush_context, instances):
    """
    Intercepta Insert, Update e Delete para gerar logs.
    """
    # 1. Detectar NOVOS registros (INSERT)
    for obj in session.new:
        if isinstance(obj, AuditLog):
            continue

        state = inspect(obj)
        new_values = {}

        for k, v in state.attrs.items():
            if k.startswith("_"):
                continue
            # Verifica se há valor e serializa
            if v.history.has_changes():
                new_values[k] = _make_serializable(v.value)

        if not new_values:
            continue

        log = AuditLog(
            table_name=obj.__tablename__,
            record_id=0,
            action="INSERT",
            old_values=None,
            new_values=new_values,
        )
        session.add(log)

    # 2. Detectar ALTERAÇÕES (UPDATE)
    for obj in session.dirty:
        if isinstance(obj, AuditLog):
            continue

        old_values, new_values = get_history(obj)

        if not new_values:
            continue

        log = AuditLog(
            table_name=obj.__tablename__,
            record_id=obj.id,
            action="UPDATE",
            old_values=old_values,
            new_values=new_values,
        )
        session.add(log)

    # 3. Detectar EXCLUSÕES FÍSICAS
    for obj in session.deleted:
        if isinstance(obj, AuditLog):
            continue

        log = AuditLog(
            table_name=obj.__tablename__,
            record_id=obj.id,
            action="PHYSICAL_DELETE",
            old_values={"status": "deleted_physically"},
            new_values=None,
        )
        session.add(log)
