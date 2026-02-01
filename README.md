
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
| 10 | [**Secure Webhooks**](./10-secure-webhooks) | Sistema de envio de notificações para terceiros com garantia de integridade via assinatura HMAC (SHA-256). | ✅ Concluído |
| 11 | [**Saga Pattern**](./11-saga-pattern) | Orquestração de transações distribuídas entre microserviços (Pedido -> Estoque -> Pagamento) com compensação de falhas. | ✅ Concluído |
| 12 | [**Transactional Outbox**](./12-transactional-outbox) | Garantia de consistência eventual entre persistência em banco de dados e publicação de eventos (Kafka/RabbitMQ). | ✅ Concluído |
| 13 | [**Feature Flags**](./13-feature-flags) | Sistema de toggles para ativação gradual de recursos (Canary Release) e testes A/B baseados em usuários. | ✅ Concluído |
| 14 | [**API Rate Limiting**](./14-api-rate-limiting) | Controle de tráfego distribuído utilizando Redis (Fixed Window Algorithm) para prevenir abuso de API. | ✅ Concluído |
| 15 | [**Circuit Breaker**](./15-circuit-breaker) | Padrão de resiliência (State Machine) para prevenir falhas em cascata e permitir auto-recuperação (Self-Healing). | ✅ Concluído |
| 16 | [**CQRS**](./16-cqrs) | Segregação de responsabilidades entre Comandos (Escrita/Regras) e Consultas (Leitura/Performance). | ✅ Concluído |
| 17 | [**Domain Events**](./17-domain-events) | Desacoplamento de serviços utilizando Event Bus e Observer Pattern (Core Logic vs Side Effects). | ✅ Concluído |
| 18 | [**Idempotency API**](./18-idempotency-hardcore) | Garantia de execução única em transações financeiras utilizando Distributed Locking (Redis SETNX) para evitar Race Conditions. | ✅ Concluído |
| 19 | [**Distributed Tracing**](./19-distributed-tracing) | Observabilidade e monitoramento de performance (APM) utilizando OpenTelemetry e Jaeger para identificar gargalos. | ✅ Concluído |
| 20 | [**Graceful Shutdown**](./20-graceful-shutdown) | Gerenciamento de sinais do sistema (SIGTERM) para finalização segura de requisições em andamento antes do encerramento do processo. | ✅ Concluído |

