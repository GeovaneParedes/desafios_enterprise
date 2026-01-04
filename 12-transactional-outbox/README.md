# Day 12: Transactional Outbox Pattern

Implementação do padrão **Transactional Outbox** para garantir atomicidade entre operações de Banco de Dados e Publicação de Mensagens (Broker).

Este padrão resolve o "Dual Write Problem", onde uma falha de rede após salvar no banco (mas antes de publicar no Kafka) deixaria o sistema inconsistente.

## 🚀 Funcionalidades

### 1. Atomicidade (ACID)
* O `OrderService` salva o Pedido e o Evento (`OutboxEvent`) na **mesma transação** de banco de dados.
* Garantia matemática: Ou ambos são salvos, ou nenhum é.

### 2. Relay Worker (Async)
* Um processo separado (`OutboxRelay`) monitora a tabela de eventos.
* Lê eventos pendentes (`processed=False`) e os publica no Broker.
* Implementa semântica **At-Least-Once Delivery**: Só marca como processado após confirmação de sucesso do Broker.

### 3. Resiliência
* Se o Broker estiver fora do ar, o evento permanece persistido no banco e será tentado novamente (Retry).

## 🛠️ Tecnologias

* **Python 3.11+**
* **SQLAlchemy 2.0+** (Gerenciamento de Transações)
* **Pytest & Mocks** (Simulação de falhas do Broker)

## 📂 Estrutura do Projeto

```text
src/
├── models.py    # Schemas (Order e OutboxEvent)
├── services.py  # Regra de negócio com transação atômica
├── relay.py     # Worker que processa a fila do banco para o broker
└── main.py      # Demo do fluxo completo
tests/
└── test_outbox.py # Testes de atomicidade e retries em caso de falha
```
## ⚡ Como Executar
## 1. Instalação

```bash
make install
```

## 2. Simulação Visual

```
make run
```

## 3. Testes Automatizados

```bash
make test
```

