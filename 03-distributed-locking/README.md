# Desafio Enterprise #03: Distributed Locking (Mutex)

## O Problema (Business Case)
Em sistemas distribuídos com alta concorrência (ex: e-commerce na Black Friday, reserva de assentos em cinema/voos), múltiplos processos tentam acessar e modificar um recurso compartilhado simultaneamente.

Sem um mecanismo de controle, ocorre a **Race Condition (Condição de Corrida)**:
1. Usuário A lê estoque: 1 item.
2. Usuário B lê estoque: 1 item (antes do A salvar a compra).
3. Usuário A compra -> Estoque 0.
4. Usuário B compra -> Estoque -1.

Resultado: **Overbooking** (venda duplicada), prejuízo financeiro e experiência ruim para o cliente.

## A Solução Técnica
Implementação de um **Distributed Lock (Mutex)** utilizando Redis.
O Lock garante que apenas **um processo por vez** possa entrar na "Zona Crítica" (o trecho de código que verifica e debita o estoque).

### Detalhes da Implementação
- **Algoritmo:** Redis `SET resource_name my_token NX PX 5000`.
    - `NX`: Só define se a chave NÃO existir (garante exclusividade).
    - `PX`: Define um TTL (Time-to-Live) para evitar Deadlocks se o processo morrer antes de liberar a trava.
- **Safety:** O desbloqueio (`release`) usa um **Lua Script** para garantir que apenas o "dono" da trava (token UUID) possa removê-la.
- **Stack:** Python (FastAPI) + Redis.

---

## Como Rodar

### 1. Setup
```bash
# Instalar dependências
make install
