# Day 18: Hardcore Idempotency (Distributed Locking)

Implementação de um mecanismo de **Idempotência Pessimista** utilizando Redis Lock para prevenir Condições de Corrida (Race Conditions) em APIs críticas (Pagamentos/Transações).

Diferente de implementações simples de cache, esta abordagem protege o sistema contra **Requisições Concorrentes (Double-Click)**, onde múltiplos processos tentam executar a mesma ação simultaneamente.

## 🚀 Funcionalidades

### 1. Máquina de Estados (Tri-State)
O sistema gerencia 3 estados para cada chave de idempotência:
1.  **NULL:** Chave livre. O primeiro a chegar adquire o Lock (`SETNX`).
2.  **IN_PROGRESS:** Bloqueio temporário. Requisições concorrentes recebem `409 Conflict` (Fail Fast).
3.  **COMPLETED:** Processamento finalizado. O Lock é substituído pelo payload de resposta (JSON), que será retornado em retries futuros.

### 2. Proteção contra Race Condition
* Utiliza `Redis SET ... NX EX` para garantir atomicidade na aquisição da trava.
* Impede que duas threads processem o mesmo pagamento se chegarem no mesmo milissegundo.

### 3. Cache Result Pattern
* Após o processamento, a resposta (Status Code + Body) é salva no Redis com TTL de 24h.
* Garante consistência: O cliente pode tentar 1000 vezes, receberá sempre a mesma resposta da primeira execução bem-sucedida.

## 🛠️ Tecnologias

* **Python 3.11+ (Flask)**
* **Redis 7** (Locking e Caching)
* **Pytest & Threads** (Simulação de concorrência real)

## 📂 Estrutura do Projeto

```text
src/
├── app.py          # API com endpoint lento (sleep) para forçar concorrência
├── idempotency.py  # Decorator com a lógica de Locking e Cache
└── middleware.py   # Versão anterior (não utilizada neste hard mode)
tests/
└── test_race.py    # Teste de Stress lançando threads simultâneas
docker-compose.yml  # Redis dedicado
```
## ⚡ Como Executar

## 1. Infraestrutura

```bash
make up
make install
```

## 2. Rodar API (Terminal 1)

Necessário para receber as chamadas das threads de teste.
```bash
make run
```
## 3. Rodar Teste de Concorrência (Terminal 2)

Dispara requisições simultâneas e valida se ocorre o bloqueio (409) e o sucesso (200).
```bash
make test
```

