import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis

from distributed_lock import DistributedLock

# Configuração
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Vamos resetar o estoque para 1 ingresso sempre que iniciar
    redis_client.set("estoque_show_coldplay", 1)
    print("🎸 Estoque inicial definido: 1 ingresso disponível")
    yield
    # Shutdown
    redis_client.close()


app = FastAPI(
    title="Enterprise Challenge #03 - Distributed Lock", lifespan=lifespan
)


class PurchaseRequest(BaseModel):
    user_id: str


@app.post("/comprar")
def comprar_ingresso(request: PurchaseRequest):
    resource_id = "estoque_show_coldplay"

    # Tenta adquirir a trava para mexer no estoque
    # O timeout=2 garante que não vamos esperar pra sempre se o sistema travar
    lock = DistributedLock(redis_client, lock_name=resource_id)

    if lock.acquire(blocking=True, timeout=5):
        try:
            # --- ZONA CRÍTICA (Apenas um processo entra aqui por vez) ---
            print(f"👤 Usuário {request.user_id} entrou na zona crítica...")

            # 1. Lê o estoque atual
            estoque = int(redis_client.get(resource_id) or 0)

            # Simula processamento (validação de cartão, antifraude...)
            # Sem o lock, isso causaria a Race Condition
            time.sleep(0.5)

            if estoque > 0:
                # 2. Debita
                novo_estoque = estoque - 1
                redis_client.set(resource_id, novo_estoque)
                print(
                    f"✅ Venda realizada para {request.user_id}!"
                    f" Estoque restante: {novo_estoque}"
                )
                return {
                    "status": "sucesso",
                    "mensagem": "Ingresso comprado!",
                    "user": request.user_id,
                }
            else:
                print(
                    f"❌ Usuário {request.user_id} tentou comprar, mas acabou."
                )
                raise HTTPException(
                    status_code=409, detail="Esgotado! Você chegou tarde."
                )

        finally:
            # Sempre libera a trava, mesmo se der erro no código acima
            lock.release()
    else:
        # Se não conseguiu pegar a trava após o timeout
        raise HTTPException(
            status_code=429,
            detail="O sistema está congestionado. Tente novamente.",
        )


@app.get("/estoque")
def ver_estoque():
    return {"estoque": redis_client.get("estoque_show_coldplay")}
