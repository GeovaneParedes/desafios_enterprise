Cronograma: 20 Dias de Desafios Enterprise

    API Rate Limiting Distribuído: Controle de tráfego para proteger recursos (evitar DDoS e abuso).

    Idempotência em Pagamentos: Garantir que uma requisição de pagamento duplicada não cobre o cliente duas vezes.

    Distributed Locking (Mutex Distribuído): Impedir que dois usuários comprem o mesmo assento de cinema simultaneamente.

    Padrão Circuit Breaker: Evitar falhas em cascata quando um microserviço dependente cai.

    CQRS (Command Query Responsibility Segregation): Separar modelos de leitura e escrita para performance extrema.

    Processamento Assíncrono com Filas (Dead Letter Queues): Lidar com falhas de processamento em background e retentativas (Retry Pattern).

    Cache Aside & Cache Stampede Prevention: Estratégias avançadas de cache para evitar derrubar o banco de dados.

    Soft Delete e Auditoria: Implementar exclusão lógica com histórico de alterações (Temporal Tables).

    Sharding de Banco de Dados (Simulação): Roteamento de dados baseado em chaves (Tenant ID) para escalabilidade horizontal.

    Webhooks com Assinatura HMAC: Sistema de envio de notificações seguro para terceiros.

    Saga Pattern (Orquestração): Transação distribuída entre 3 serviços (ex: Pedido -> Estoque -> Pagamento).

    Outbox Pattern: Garantir consistência entre salvar no banco e publicar evento no Kafka/RabbitMQ.

    Dynamic Feature Flags: Ativar/Desativar funcionalidades em tempo de execução sem deploy.

    Busca Textual (Full Text Search): Implementação eficiente de busca em milhões de registros (Elasticsearch ou Postgres TSVECTOR).

    Validação de Arquivos Grandes (Streaming): Upload e processamento de arquivos de Gigabytes sem estourar a RAM.

    Gerenciamento de Segredos (Vault): Injeção segura de credenciais em tempo de execução.

    API Gateway (Aggregator Pattern): Um endpoint único que consolida dados de 4 serviços internos.

    Health Checks Profundos: Monitoramento que verifica dependências (DB, Cache) e não apenas se a API responde 200.

    Tenant Isolation (Multi-tenancy): Garantir que o Cliente A nunca veja dados do Cliente B na mesma tabela.

    Graceful Shutdown: Garantir que o servidor termine as requisições em andamento antes de morrer (SIGTERM).
