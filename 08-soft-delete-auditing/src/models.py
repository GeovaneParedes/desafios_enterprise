from datetime import datetime, timezone
from typing import Any, Optional

# REMOVIDO: Text (não estava sendo usado)
from sqlalchemy import JSON, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core import AuditMixin, Base, SoftDeleteMixin


# --- Tabela de Logs (Nova) ---
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    table_name: Mapped[str] = mapped_column(String(50), nullable=False)
    record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    # INSERT, UPDATE, DELETE
    action: Mapped[str] = mapped_column(String(10), nullable=False)

    old_values: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )
    new_values: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )
    changed_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Audit {self.action} on {self.table_name}:{self.record_id}>"


# --- Tabela de Negócio ---
class BankAccount(Base, SoftDeleteMixin, AuditMixin):
    __tablename__ = "bank_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_name: Mapped[str] = mapped_column(String(100), nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0)

    def __repr__(self):
        status = "❌" if self.is_deleted else "✅"
        # CORREÇÃO: Quebra de linha para satisfazer o limite de 79 chars
        return (
            f"<Account {self.id} | {self.owner_name} | "
            f"${self.balance} | {status}>"
        )
