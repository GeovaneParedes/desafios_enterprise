from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, event
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    ORMExecuteState,
    Session,
    mapped_column,
    with_loader_criteria,
)


class Base(DeclarativeBase):
    pass


class SoftDeleteMixin:
    """
    Adiciona suporte a exclusão lógica.
    """

    is_deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, index=True
    )
    # DateTime com timezone=True é a boa prática para Postgres
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def soft_delete(self, session: Session):
        """Marca o registro como deletado usando UTC aware."""
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)
        session.add(self)


class AuditMixin:
    """
    Adiciona colunas de auditoria básica.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        # Lambda garante que a função seja chamada na hora do insert
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


# --- Global Filter (Query Interceptor) ---


@event.listens_for(Session, "do_orm_execute")
def add_filtering_criteria(execute_state: ORMExecuteState):
    """
    Intercepta todas as queries ORM.
    Se for um SELECT e a tabela tiver SoftDeleteMixin,
    adiciona automaticamente 'WHERE is_deleted = False'.
    """
    if (
        execute_state.is_select
        and not execute_state.is_column_load
        and not execute_state.is_relationship_load
    ):
        include_deleted = execute_state.execution_options.get(
            "include_deleted", False
        )

        if not include_deleted:
            # CORREÇÃO: Removemos a linha 'enable_relationship_loading' que
            # causava o erro.
            # Apenas aplicamos a opção de filtro na query.
            execute_state.statement = execute_state.statement.options(
                with_loader_criteria(
                    SoftDeleteMixin,
                    lambda cls: cls.is_deleted.is_(False),
                    include_aliases=True,
                )
            )
