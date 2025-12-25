import sys
import os

# Adiciona o diretório atual ao path para imports funcionarem
sys.path.append(os.getcwd())

from src.router import ShardRouter
from src.models import User
from sqlalchemy import text

# Configuração das URLs (Portas definidas no docker-compose)
SHARD_URLS = [
    "postgresql://admin:password@localhost:5433/app_db_shard_1",
    # Shard 0 (Par)
    "postgresql://admin:password@localhost:5434/app_db_shard_2",
    # Shard 1 (Ímpar)
]


def run_demo():
    print("--- 🚀 Iniciando Demo de Database Sharding ---")

    # 1. Inicializa o Router
    router = ShardRouter(SHARD_URLS)
    router.create_tables()
    print("-" * 50)

    # 2. Dados de Teste (Tenants Pares e Ímpares)
    users_data = [
        {
            "tenant_id": 10,
            "name": "Empresa A (Par)",
            "email": "contact@a.com",
        },  # 10 % 2 = 0 -> Shard 0
        {
            "tenant_id": 11,
            "name": "Empresa B (Ímpar)",
            "email": "contact@b.com",
        },  # 11 % 2 = 1 -> Shard 1
        {
            "tenant_id": 22,
            "name": "Empresa C (Par)",
            "email": "contact@c.com",
        },  # 22 % 2 = 0 -> Shard 0
        {
            "tenant_id": 33,
            "name": "Empresa D (Ímpar)",
            "email": "contact@d.com",
        },  # 33 % 2 = 1 -> Shard 1
    ]

    # 3. Inserção com Roteamento Automático
    print("📥 Inserindo Usuários...")
    for data in users_data:
        t_id = data["tenant_id"]

        # MÁGICA AQUI: Pedimos a sessão para o router baseada no ID
        session = router.get_session(t_id)

        shard_used = session.info["shard_id"]
        print(f"   👤 Tenant {t_id} -> Roteado para Shard {shard_used}")

        user = User(**data)
        session.add(user)
        session.commit()
        session.close()

    print("-" * 50)

    # 4. Verificação Física (Query direta em cada banco para provar a
    # separação)
    print("🔎 Auditoria Física dos Shards:")

    for idx, engine in enumerate(router.engines):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT tenant_id, name FROM users"))
            rows = result.fetchall()

            print(f"\n📦 [SHARD {idx}] (Porta {5433 + idx}) contém"
                  f" {len(rows)} registros:")
            for row in rows:
                print(f"   - Tenant {row.tenant_id}: {row.name}")


if __name__ == "__main__":
    run_demo()
