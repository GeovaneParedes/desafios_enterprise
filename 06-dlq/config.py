import asyncio
import os

import aio_pika

# Configurações de Conexão
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

# Nomes das Filas e Exchanges
EXCHANGE_NAME = "orders_exchange"
QUEUE_NAME = "orders_queue"
DLQ_EXCHANGE_NAME = "orders_dlq_exchange"
DLQ_QUEUE_NAME = "orders_dlq"


async def get_rabbitmq_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)


async def setup_infrastructure(channel: aio_pika.abc.AbstractChannel):
    """
    Declara a topologia completa com DLQ configurada.
    Isso garante que as filas existam antes de tentarmos usar.
    """
    # 1. Declarar Exchange da DLQ (Dead Letter)
    dlq_exchange = await channel.declare_exchange(
        DLQ_EXCHANGE_NAME, aio_pika.ExchangeType.DIRECT, durable=True
    )

    # 2. Declarar Fila da DLQ
    dlq_queue = await channel.declare_queue(DLQ_QUEUE_NAME, durable=True)

    # 3. Bind da DLQ (Liga a fila ao exchange)
    await dlq_queue.bind(dlq_exchange, routing_key="dead_letter")

    # 4. Declarar Exchange Principal
    main_exchange = await channel.declare_exchange(
        EXCHANGE_NAME, aio_pika.ExchangeType.DIRECT, durable=True
    )

    # 5. Declarar Fila Principal com argumentos de DLQ
    # AQUI ESTÁ O PULO DO GATO: Se der erro/rejeição, manda pra DLQ
    args = {
        "x-dead-letter-exchange": DLQ_EXCHANGE_NAME,
        "x-dead-letter-routing-key": "dead_letter",
    }

    main_queue = await channel.declare_queue(
        QUEUE_NAME, durable=True, arguments=args
    )

    # 6. Bind Principal
    await main_queue.bind(main_exchange, routing_key="process_order")

    return main_exchange, main_queue
