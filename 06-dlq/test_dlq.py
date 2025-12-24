import asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from config import DLQ_QUEUE_NAME, get_rabbitmq_connection
from producer import app

BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_dlq_workflow():

    # --- ETAPA 0: LIMPEZA PRÉVIA ---
    # Garante que a DLQ está vazia antes de começar para não pegar lixo antigo
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        try:
            dlq_queue = await channel.declare_queue(
                DLQ_QUEUE_NAME, durable=True, passive=True
            )
            await dlq_queue.purge()
            print("\n🧹 DLQ Limpa antes do teste.")
        except Exception:
            # Se a fila não existir ainda, tudo bem
            pass

    async with app.router.lifespan_context(app):

        # 1. Dispara o pedido "BOMBA"
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=BASE_URL
        ) as client:
            payload = {"item_name": "BOMBA", "quantity": 1, "price": 0}
            response = await client.post("/orders", json=payload)

            assert response.status_code == 202
            data = response.json()
            order_id = data["id"]
            print(f"🚀 Pedido Disparado: {order_id}")

        # 2. Espera o Worker rejeitar
        print("⏳ Aguardando worker rejeitar a mensagem...")
        await asyncio.sleep(2)

        # 3. Auditoria na DLQ
        # Precisamos abrir uma NOVA conexão pois a anterior foi fechada
        # no context manager
        connection = await get_rabbitmq_connection()
        async with connection:
            channel = await connection.channel()
            dlq_queue = await channel.declare_queue(
                DLQ_QUEUE_NAME, durable=True, passive=True
            )

            message = await dlq_queue.get(fail=False)

            assert message is not None, "A DLQ está vazia!"

            body = message.body.decode()
            print(f"💀 Mensagem encontrada na DLQ: {body}")

            assert order_id in body
            assert "BOMBA" in body

            await message.ack()
