import json

from database import redis_client


class ProductQueryHandler:
    def get_product_by_id(self, product_id: str):
        """Lê direto do Redis (Milissegundos)"""
        data = redis_client.get(f"product:{product_id}")
        if not data:
            return None
        return json.loads(data)

    def get_catalog(self):
        """Lista todo o catálogo direto do Redis"""
        # Pega todos os itens da lista 'catalog'
        items = redis_client.lrange("catalog", 0, -1)
        return [json.loads(i) for i in items]
