from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from commands import CreateProductCommand, ProductCommandHandler
from database import init_db, reset_read_model
from queries import ProductQueryHandler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa SQL e Limpa Redis ao subir
    init_db()
    # reset_read_model() # Opcional: descomente se quiser limpar o
    # redis ao reiniciar
    print("🚀 CQRS System Online: SQL (Write) + Redis (Read)")
    yield
    print("🛑 System Shutdown")


app = FastAPI(title="Enterprise Challenge #05 - CQRS", lifespan=lifespan)

# Handlers
command_handler = ProductCommandHandler()
query_handler = ProductQueryHandler()


# --- WRITE SIDE (COMMANDS) ---
@app.post("/products", status_code=201)
def create_product(cmd: CreateProductCommand):
    """
    Endpoint de ESCRITA.
    Processa regras complexas e grava no SQL.
    """
    try:
        return command_handler.handle_create(cmd)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- READ SIDE (QUERIES) ---
@app.get("/products/{product_id}")
def get_product(product_id: str):
    """
    Endpoint de LEITURA.
    Vai direto no Redis. Ultra rápido. Não toca no SQL.
    """
    product = query_handler.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@app.get("/catalog")
def list_catalog():
    """
    Endpoint de LEITURA (Lista).
    """
    return query_handler.get_catalog()
