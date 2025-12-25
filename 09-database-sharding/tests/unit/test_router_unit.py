import pytest
from src.router import ShardRouter


class TestShardRouterUnit:
    def test_routing_algorithm_modulo(self):
        """
        Valida se o algoritmo de módulo distribui corretamente
        baseado na quantidade de shards.
        """
        # Mock de URLs (não conecta de verdade no unitário)
        mock_urls = ["sqlite:///:memory:", "sqlite:///:memory:"]
        router = ShardRouter(mock_urls)

        # 2 Shards:
        # 10 % 2 = 0
        # 11 % 2 = 1
        assert router.get_shard_index(10) == 0
        assert router.get_shard_index(11) == 1
        assert router.get_shard_index(2) == 0

    def test_routing_scaling(self):
        """
        Valida comportamento com 3 shards.
        """
        # CORREÇÃO: O Router tenta criar engines no __init__,
        # então precisamos passar
        # strings de conexão válidas.
        # Usamos SQLite em memória repetido 3 vezes.
        mock_urls = [
            "sqlite:///:memory:",
            "sqlite:///:memory:",
            "sqlite:///:memory:",
        ]
        router = ShardRouter(mock_urls)

        # Lógica do Modulo (3 Shards):
        # 10 % 3 = 1 (Resto 1)
        # 12 % 3 = 0 (Resto 0)
        # 14 % 3 = 2 (Resto 2)

        assert router.get_shard_index(10) == 1
        assert router.get_shard_index(12) == 0
        assert router.get_shard_index(14) == 2
