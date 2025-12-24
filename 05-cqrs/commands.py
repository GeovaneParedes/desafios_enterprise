import json
import uuid

from pydantic import BaseModel

from database import get_db_connection, redis_client


# DTO para entrada de dados
class CreateProductCommand(BaseModel):
    sku: str
    name: str
    price: float
    stock: int


class ProductCommandHandler:
    def handle_create(self, cmd: CreateProductCommand):
        """
        1. Valida Regras de Negócio
        2. Persiste no Write Model (SQL)
        3. Sincroniza com Read Model (Redis)
        """
        product_id = str(uuid.uuid4())

        # --- Passo 1: Write Model (SQL) ---
        # Foco: Integridade e Transação
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO products (id, sku, name, price, stock)"
                    " VALUES (?, ?, ?, ?, ?)",
                    (product_id, cmd.sku, cmd.name, cmd.price, cmd.stock),
                )
                conn.commit()
            except Exception as e:
                # Se falhar no SQL, aborta tudo
                raise ValueError(f"Erro ao criar produto: {str(e)}")

        # --- Passo 2: Atualizar Read Model (Redis) ---
        # Foco: Performance de Leitura.
        # Guardamos um JSON pronto para ser consumido pela API de leitura.
        product_view = {
            "id": product_id,
            "sku": cmd.sku,
            "name": cmd.name,
            "price": cmd.price,
            "available": cmd.stock > 0,
            "desc": f"{cmd.name} - ${cmd.price}",
        }

        # Salvamos no Redis com a chave "product:{id}"
        redis_client.set(f"product:{product_id}", json.dumps(product_view))

        # Também adicionamos a uma lista de catálogo para listar rápido
        redis_client.rpush("catalog", json.dumps(product_view))

        return {"id": product_id, "status": "created"}
