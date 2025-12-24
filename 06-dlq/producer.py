import json
import uuid
from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import EXCHANGE_NAME, get_rabbitmq_connection, setup_infrastructure


# Modelo de Dados
class OrderRequest(BaseModel):
    item_name: str
    quantity: int
    price: float


# Gerenciamento de Vida da Aplicação
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Conecta ao RabbitMQ ao iniciar
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()

    # Garante que a infraestrutura (Exchanges/Filas/DLQ) existe
    await setup_infrastructure(channel)

    # Guarda a conexão no estado da app para reuso
    app.state.rabbit_connection = connection
    app.state.rabbit_channel = channel

    print("🚀 Producer API Online & RabbitMQ Connected")
    yield

    # Fecha conexão ao desligar
    await connection.close()
    print("🛑 Connection Closed")


app = FastAPI(title="Enterprise Challenge #06 - Async DLQ", lifespan=lifespan)


@app.post("/orders", status_code=202)
async def create_order(order: OrderRequest):
    """
    Recebe o pedido e enfileira para processamento assíncrono.
    Retorna 202 Accepted imediatamente.
    """
    order_id = str(uuid.uuid4())

    # Mensagem pronta para a fila
    message_body = {
        "id": order_id,
        "item": order.item_name,
        "qty": order.quantity,
        "total": order.quantity * order.price,
    }

    # Publica na Exchange
    channel = app.state.rabbit_channel
    exchange = await channel.get_exchange(EXCHANGE_NAME)

    await exchange.publish(
        aio_pika.Message(
            body=json.dumps(message_body).encode(),
            content_type="application/json",
            # Headers persistentes garantem que a mensagem não suma
            # se o Rabbit cair
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key="process_order",
    )

    return {
        "id": order_id,
        "status": "queued",
        "message": "Pedido recebido para processamento",
    }
