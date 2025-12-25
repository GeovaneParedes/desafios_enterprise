import pytest
from sqlalchemy import text
from src.router import ShardRouter
from src.models import User

# URLs apontando para os containers Docker que já subimos
SHARD_URLS = [
    "postgresql://admin:password@localhost:5433/app_db_shard_1",
    "postgresql://admin:password@localhost:5434/app_db_shard_2",
]


@pytest.fixture(scope="module")
def router():
    """Fixture que inicializa o roteador e limpa os bancos antes do teste."""
    r = ShardRouter(SHARD_URLS)
    r.create_tables()

    # Limpeza pré-teste (TRUNCATE) em todos os shards
    for engine in r.engines:
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY"))
            conn.commit()

    return r


def test_shard_physical_separation(router):
    """
    Teste End-to-End:
    1. Insere dados via Router.
    2. Verifica fisicamente em cada Shard se o dado caiu no lugar certo.
    """
    # 1. Inserção
    # Tenant 10 -> Shard 0 (Par)
    # Tenant 11 -> Shard 1 (Ímpar)

    session_even = router.get_session(tenant_id=10)
    user_even = User(tenant_id=10, name="User Par", email="even@test.com")
    session_even.add(user_even)
    session_even.commit()
    session_even.close()

    session_odd = router.get_session(tenant_id=11)
    user_odd = User(tenant_id=11, name="User Ímpar", email="odd@test.com")
    session_odd.add(user_odd)
    session_odd.commit()
    session_odd.close()

    # 2. Verificação Física (Bypassing Router)
    # Conecta direto no Shard 0 e vê se o Tenant 10 está lá
    with router.engines[0].connect() as conn:
        result = conn.execute(text("SELECT tenant_id FROM users")).fetchall()
        assert len(result) == 1
        assert result[0].tenant_id == 10

    # Conecta direto no Shard 1 e vê se o Tenant 11 está lá
    with router.engines[1].connect() as conn:
        result = conn.execute(text("SELECT tenant_id FROM users")).fetchall()
        assert len(result) == 1
        assert result[0].tenant_id == 11
