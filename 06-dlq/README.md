# Desafio Enterprise #06: Async Processing & Dead Letter Queues (DLQ)

## O Problema (Business Case)
Operações pesadas (processamento de imagem, envio de e-mails em massa, geração de relatórios) não devem bloquear a API principal. Se a API esperar 10 segundos para responder, o cliente desiste (timeout) e a escalabilidade do sistema é comprometida.

Além disso, falhas acontecem. Se o processamento falhar, a mensagem não pode ser perdida silenciosamente.

## A Solução Técnica
Utilizamos uma arquitetura orientada a eventos com **RabbitMQ**:
1.  **Producer (API):** Recebe o pedido, publica na fila e responde "202 Accepted" imediatamente.
2.  **Worker (Background):** Consome a fila e processa a tarefa pesada.
3.  **DLQ (Dead Letter Queue):** Se o Worker encontrar um erro irrecuperável (ou rejeitar a mensagem explicitamente), a mensagem é movida automaticamente para uma fila de "mortos" (DLQ) para análise posterior, garantindo **Zero Data Loss**.

## Arquitetura da Topologia

```mermaid
graph LR
    Client -->|POST /orders| API[Producer API]
    API -->|Publish| Exchange[Main Exchange]
    Exchange -->|Route: process_order| Queue[Main Queue]
    Queue -->|Consume| Worker[Worker Service]
    
    Worker -->|Ack (Sucesso)| Done((Fim))
    Worker -->|Nack (Erro)| DLQ_Ex[DLQ Exchange]
    DLQ_Ex -->|Route: dead_letter| DLQ[Dead Letter Queue]
```

## Tecnologias

    Python 3.10+

    FastAPI (Producer)

    Aio-Pika (RabbitMQ Async Driver)

    RabbitMQ (Message Broker)

## Como Executar

1. Infraestrutura

Suba o RabbitMQ (com painel de gestão):
```bash
docker run -d --name rabbit-dlq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    Acesse o painel em: http://localhost:15672 (User: guest / Pass: guest)
```
2. Rodar a Aplicação

Você precisará de dois terminais:

Terminal 1 (API):
```bash
make run-api
```
Terminal 2 (Worker):
```bash
make run-worker
```
Como Testar
Cenário 1: Sucesso (Happy Path)

Envie um pedido normal. O Worker deve processar e dar Ack.
```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"item_name": "Notebook", "quantity": 1, "price": 5000}'
```
Cenário 2: Falha e DLQ (Unhappy Path)

Envie um item com nome "BOMBA". O Worker vai rejeitar (Nack) e a mensagem vai para a DLQ.
```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"item_name": "BOMBA", "quantity": 1, "price": 0}'
```
