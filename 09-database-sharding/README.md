# Day 09: Database Sharding (Horizontal Scaling)

Implementação de referência para **Sharding Horizontal** na camada de aplicação, utilizando Python e SQLAlchemy.

O Sharding resolve o problema de escalabilidade de escrita em grandes sistemas, dividindo os dados em múltiplos servidores de banco de dados (Shards) com base em uma chave de particionamento (neste caso, o `Tenant ID`).

## 🚀 Funcionalidades

### 1. Roteamento Lógico (Application-Level Routing)
* **Modulo Sharding:** Algoritmo determinístico (`TenantID % TotalShards`) para decidir em qual banco o dado será gravado.
* **Transparência:** O código de negócio solicita uma sessão para um cliente (`router.get_session(tenant_id)`) sem precisar saber o endereço IP ou porta do banco físico.

### 2. Infraestrutura Distribuída
* **Multi-Node Postgres:** Orquestração de múltiplos containers PostgreSQL simulando servidores físicos distintos (Shard 01 na porta 5433, Shard 02 na porta 5434).
* **Schema Uniforme:** Garante que a estrutura das tabelas (`users`) seja idêntica em todos os shards.

## 🛠️ Tecnologias

* **Python 3.11+**
* **SQLAlchemy 2.0+** (Core & ORM)
* **PostgreSQL 15** (Via Docker)
* **Pytest** (Testes de integração e unitários)

## 📂 Estrutura do Projeto

```text
src/
├── router.py    # O "Cérebro" do Sharding (Gerencia pool de conexões e roteamento)
├── models.py    # Definição das tabelas (replicadas em todos os shards)
└── main.py      # Script de demonstração (Insere dados e audita os bancos)
tests/
├── unit/        # Valida a matemática do algoritmo de roteamento
└── integration/ # Valida a persistência real nos containers Docker
```
## ⚡ Como Executar
1. Subir Infraestrutura (Shards)
```bash
make up
```
### Isso iniciará 2 instâncias de PostgreSQL em portas distintas.
2. Executar Demo

Insere usuários e mostra no console para qual shard cada um foi roteado.
```bash
python src/main.py
```
## 3. Rodar Testes

Valida a lógica de roteamento e a separação física dos dados.
```bash
make test
```
## 4. Limpeza

Para parar e remover os volumes (dados):
```bash
make down
```

