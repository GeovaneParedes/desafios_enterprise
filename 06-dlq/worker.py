import asyncio
import json

import aio_pika

from config import QUEUE_NAME, get_rabbitmq_connection, setup_infrastructure


async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process(ignore_processed=True):
        body = json.loads(message.body.decode())
        print(
            f"📦 [Worker] Processando pedido:"
            f"{body['id']} - Item: {body['item']}"
        )

        # Simulação de Falha Crítica
        if body["item"].upper() == "BOMBA":
            print(
                f"💥 [ERRO] Falha ao processar {body['id']}!"
                f"Rejeitando mensagem..."
            )
            # Nack com requeue=False envia para a DLQ (Dead Letter Queue)
            await message.nack(requeue=False)
            return

        # Simulação de Processamento (IO Bound)
        await asyncio.sleep(1)
        print(f"✅ [Sucesso] Pedido {body['id']} finalizado.")
        # O 'async with message.process' envia o ack automaticamente no
        # final se não houver erro


async def main():
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()

    # Garante infraestrutura antes de consumir
    await setup_infrastructure(channel)

    # Define QoS (Quality of Service) - Pega 1 mensagem por vez
    await channel.set_qos(prefetch_count=1)

    queue = await channel.get_queue(QUEUE_NAME)

    print("👷 Worker iniciado. Aguardando pedidos...")
    # Inicia o consumo
    await queue.consume(process_message)

    # Mantém o script rodando
    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Worker parado.")
