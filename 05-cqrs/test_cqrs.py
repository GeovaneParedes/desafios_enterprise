import json
import os

import pytest
from fastapi.testclient import TestClient

from database import DB_FILE, init_db, redis_client
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_databases():
    """Limpa tudo antes de cada teste para garantir isolamento"""
    # Limpa Redis
    redis_client.flushdb()
    # Recria Banco SQL
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()
    yield
    # Limpeza opcional pós-teste
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)


def test_cqrs_flow_create_and_read():
    """
    Testa o fluxo completo:
    1. COMMAND: Cria no SQL via API
    2. SYNC: Verifica se foi pro Redis
    3. QUERY: Lê do Redis via API
    """
    payload = {
        "sku": "TEST-SKU-001",
        "name": "Produto Teste CQRS",
        "price": 199.90,
        "stock": 50,
    }

    # 1. COMMAND (Escrita)
    response = client.post("/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    product_id = data["id"]
    assert product_id is not None

    # 2. Validação Interna (White Box Testing)
    # Verifica se a chave foi criada no Redis imediatamente
    redis_data = redis_client.get(f"product:{product_id}")
    assert redis_data is not None
    cached_product = json.loads(redis_data)
    assert cached_product["name"] == payload["name"]
    # Verifica campo desnormalizado (exclusivo do modelo de leitura)
    assert "desc" in cached_product

    # 3. QUERY (Leitura)
    read_response = client.get(f"/products/{product_id}")
    assert read_response.status_code == 200
    read_data = read_response.json()

    assert read_data["id"] == product_id
    assert read_data["price"] == payload["price"]


def test_catalog_list():
    """Testa se a lista de catálogo está sendo populada no Redis"""
    # Cria 2 produtos
    client.post(
        "/products",
        json={"sku": "A", "name": "Item A", "price": 10, "stock": 1},
    )
    client.post(
        "/products",
        json={"sku": "B", "name": "Item B", "price": 20, "stock": 1},
    )

    # Consulta Catálogo
    response = client.get("/catalog")
    assert response.status_code == 200
    catalog = response.json()

    assert len(catalog) == 2
    assert catalog[0]["sku"] == "A" or catalog[1]["sku"] == "A"
