from typing import Dict, List
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from src.models import Base


class ShardRouter:
    """
    Gerencia o roteamento de conexões para múltiplos shards de banco de dados.
    Utiliza estratégia de Modulo Sharding baseada em tenant_id.
    """

    def __init__(self, shard_urls: List[str]):
        """
        Inicializa as engines para cada URL de shard fornecida.

        Args:
            shard_urls: Lista de strings de conexão (DSN) para cada banco.
        """
        self.engines = []
        self.session_makers = []

        print(f"🔌 Inicializando Router com {len(shard_urls)} shards...")

        for i, url in enumerate(shard_urls):
            # Cria a engine física para este shard
            engine = create_engine(url, echo=False)
            self.engines.append(engine)

            # Cria o fabricador de sessões para este shard
            sm = sessionmaker(bind=engine)
            self.session_makers.append(sm)
            print(f"   ✅ Shard {i} conectado: {url}")

    def create_tables(self):
        """Cria as tabelas em TODOS os shards."""
        print("🔨 Criando schemas em todos os shards...")
        for engine in self.engines:
            Base.metadata.create_all(engine)

    def get_shard_index(self, tenant_id: int) -> int:
        """
        Determina o índice do shard baseado no ID do tenant.
        Fórmula: index = tenant_id % numero_de_shards
        """
        return tenant_id % len(self.engines)

    def get_session(self, tenant_id: int) -> Session:
        """
        Retorna uma Sessão do SQLAlchemy conectada ao shard correto.

        Args:
            tenant_id: O ID do cliente para roteamento.

        Returns:
            Session: Objeto de sessão conectado ao banco físico correto.
        """
        shard_idx = self.get_shard_index(tenant_id)
        session = self.session_makers[shard_idx]()

        # Injetamos um atributo extra na sessão para debug (opcional)
        session.info["shard_id"] = shard_idx
        return session
