import json
import os
import sqlite3
from contextlib import contextmanager

import redis

# --- Configuração WRITE SIDE (SQL) ---
DB_FILE = "enterprise_store.db"


def init_db():
    """Inicializa o banco Relacional (Write Model)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Tabela normalizada, típica de escrita
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Para retornar dicts
    try:
        yield conn
    finally:
        conn.close()


# --- Configuração READ SIDE (Redis) ---
# Usamos Redis para armazenar a "View" desnormalizada do produto
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    db=0,
    decode_responses=True,
)


def reset_read_model():
    """Limpa o cache de leitura (apenas para testes/reset)"""
    redis_client.flushdb()
