
# Enterprise Software Engineering Challenges

Este repositório documenta a implementação de referência para 20 cenários complexos de engenharia de software focados em aplicações corporativas de alta escala. 

O objetivo é demonstrar soluções robustas para problemas comuns em sistemas distribuídos, priorizando escalabilidade, consistência de dados, segurança e resiliência.

## Visão Geral do Projeto

Ao contrário de provas de conceito simples, este projeto adota uma abordagem de engenharia rigorosa:

* **Linguagem & Runtime:** Python 3.11+ (Foco em Type Hinting e Modern Asyncio).
* **Qualidade de Código:** Adesão estrita aos princípios SOLID, Clean Code e Design Patterns.
* **Infraestrutura:** Containerização via Docker e orquestração de dependências (Redis, Postgres, RabbitMQ).
* **Testabilidade:** Cobertura de testes unitários e de integração para fluxos críticos.

## Roteiro de Implementação

Abaixo estão listados os 20 desafios arquiteturais abordados neste projeto. Cada módulo contém sua própria documentação técnica detalhada, diagramas de sequência e análise de complexidade (Big-O).

| ID | Padrão / Desafio | Descrição do Problema & Solução | Status |
|:--:|:---|:---|:--:|
| 01 | [**Distributed Rate Limiting**](./01-distributed-rate-limiting) | Controle de tráfego distribuído (Sliding Window) utilizando Redis para prevenção de DDoS e abuso de recursos. | ✅ Concluído |
| 02 | [**Idempotency Middleware**](./02-idempotency) | Garante que requisições de pagamento repetidas (devido a falhas de rede) não gerem cobrança dupla, usando Redis e Chaves de Idempotência. | ✅ Concluído |
| 03 | [**Distributed Locking**](./03-distributed-locking) | Mutex distribuído para prevenir Race Conditions em acesso concorrente a recursos críticos (ex: reserva de assentos). | ✅ Concluído |
| 04 | [**Circuit Breaker**](./04-circuit-breaker) | Proteção contra falhas em cascata e degradação graciosa quando serviços dependentes ficam indisponíveis. | ✅ Concluído |
| 05 | [**CQRS**](./05-cqrs) | Segregação de responsabilidade de Comando e Consulta para otimização de performance de leitura e escrita. | ✅ Concluído |
| 06 | [**Async Processing & DLQ**](./06-dlq) | Processamento assíncrono robusto com estratégia de *Dead Letter Queues* para tratamento de falhas e *Retry Pattern*. | ✅ Concluído |
| 07 | [**Cache Strategy**](./07-cache-strategy) | Implementação de *Cache Aside* com proteção contra *Cache Stampede* (Thundering Herd Problem) via Mutex. | ✅ Concluído |
| 08 | [**Soft Delete & Auditing**](./08-soft-delete-auditing) | Implementação de exclusão lógica com *Global Query Filters* e auditoria automática de alterações (CDC) via Event Listeners. | ✅ Concluído |
| 09 | [**Database Sharding**](./09-database-sharding) | Simulação de roteamento de dados e particionamento horizontal (Application-Level) baseado em Tenant ID. | ✅ Concluído |
| 10 | **Secure Webhooks** | Sistema de envio de notificações para terceiros com garantia de integridade via assinatura HMAC (SHA-256). | A Fazer |
| 11 | **Saga Pattern** | Orquestração de transações distribuídas entre microserviços (Pedido -> Estoque -> Pagamento) com compensação de falhas. | A Fazer |
| 12 | **Transactional Outbox** | Garantia de consistência eventual entre persistência em banco de dados e publicação de eventos (Kafka/RabbitMQ). | A Fazer |
| 13 | **Feature Flags** | Sistema dinâmico para ativação/desativação de funcionalidades em tempo de execução sem necessidade de deploy (Decoupling Deploy from Release). | A Fazer |
| 14 | **Full Text Search** | Implementação eficiente de indexação e busca textual em grandes volumes de dados (simulação de engine de busca). | A Fazer |
| 15 | **Large File Streaming** | Upload e processamento de arquivos na ordem de Gigabytes utilizando *streams* para baixo consumo de memória (RAM). | A Fazer |
| 16 | **Secrets Management** | Padrões para injeção segura de credenciais e segredos em tempo de execução, evitando dados sensíveis no código. | A Fazer |
| 17 | **API Gateway (Aggregator)** | Padrão de Gateway para consolidação de chamadas a múltiplos microserviços em um único endpoint otimizado. | A Fazer |
| 18 | **Deep Health Checks** | Monitoramento avançado verificando conectividade de dependências críticas (DB, Cache, Broker) e latência. | A Fazer |
| 19 | **Multi-tenancy Isolation** | Arquitetura garantindo isolamento estrito de dados entre diferentes clientes (Tenants) em ambiente compartilhado. | A Fazer |
| 20 | **Graceful Shutdown** | Gerenciamento de sinais do sistema (SIGTERM) para finalização segura de requisições em andamento antes do encerramento do processo. | A Fazer |
