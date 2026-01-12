import pytest
from src.handlers import CommandHandler, QueryHandler, CreateUserCommand


def test_cqrs_flow():
    # Arrange
    cmd_handler = CommandHandler()
    q_handler = QueryHandler()

    # Act (Write)
    cmd = CreateUserCommand("alice", "alice@test.com", "123456")
    uid = cmd_handler.handle_create_user(cmd)

    # Act (Read)
    result = q_handler.get_user_summary(uid)

    # Assert
    assert result["id"] == uid
    assert result["display_name"] == "ALICE"  # Verifica a projeção
    assert "password_hash" not in result     # Verifica segurança
    assert result["contact"] == "alice@test.com"


def test_read_model_isolation():
    """Garante que alterar o comando não afeta a leitura
    até que seja processado
    """
    q_handler = QueryHandler()

    # ID inexistente
    assert q_handler.get_user_summary(999) is None
