import asyncio
import os
import random
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from redis import Redis

from idempotency import IdempotencyMiddleware

# Configuração Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = Redis(
    host=REDIS_HOST, port=6379, db=0, decode_responses=False
)  # Decode False para bytes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Conectando ao Redis...")
    if redis_client.ping():
        print("Redis conectado com sucesso!")
    yield
    # Shutdown
    redis_client.close()


app = FastAPI(title="Enterprise Challenge #02 - Idempotency", lifespan=lifespan)

# --- ADICIONA O MIDDLEWARE ---
# Injetamos o Redis e o tempo de expiração
app.add_middleware(IdempotencyMiddleware, redis_client=redis_client)


@app.post("/api/v1/payment")
async def process_payment(request: Request):
    """
    Simula uma transação financeira complexa.
    Sem idempotência, cada chamada cobraria o cliente novamente.
    """
    body = await request.json()
    user_id = body.get("user_id")
    amount = body.get("amount")

    # Simula latência de processamento bancário (1 a 3 segundos)
    # É aqui que o timeout do cliente costuma acontecer
    delay = random.uniform(1.0, 3.0)
    await asyncio.sleep(delay)

    # Gera um ID de transação "único" (Simulação)
    transaction_id = f"TX-{random.randint(1000, 9999)}"

    return {
        "status": "processed",
        "transaction_id": transaction_id,
        "amount_deducted": amount,
        "user": user_id,
        "message": "Pagamento realizado com sucesso. Não me chame de novo!",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
