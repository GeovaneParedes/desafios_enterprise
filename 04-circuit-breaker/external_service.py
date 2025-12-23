import random
import time

import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Serviço Instável (Simulador)")

# Simula estado do serviço: True = Saudável, False = Morto
is_healthy = True


@app.get("/health")
def health_check():
    """Rota para alternar o status do serviço (simular queda)"""
    global is_healthy
    # A cada chamada, tem 20% de chance de mudar o estado
    # Ou podemos forçar a mudança manualmente se preferir
    return {"status": "healthy" if is_healthy else "dead"}


@app.post("/toggle")
def toggle_health():
    """Derruba ou levanta o serviço manualmente"""
    global is_healthy
    is_healthy = not is_healthy
    state = "SAUDÁVEL" if is_healthy else "MORTO"
    print(f"💥 ESTADO ALTERADO PARA: {state}")
    return {"message": f"Serviço agora está {state}"}


@app.get("/dados")
async def pegar_dados():
    """Simula uma operação demorada ou falha"""
    if not is_healthy:
        # Simula timeout ou erro 500
        time.sleep(2)  # Demora pra responder (Timeout)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error - O Banco explodiu 🔥",
        )

    # Simula latência normal
    time.sleep(0.1)
    return {
        "data": "Aqui estão seus dados valiosos",
        "value": random.randint(1, 100),
    }


if __name__ == "__main__":
    print("😈 Serviço Instável rodando na porta 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
