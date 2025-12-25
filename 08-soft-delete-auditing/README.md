# Day 08: Soft Delete & Auditing Strategy

Implementação de um padrão robusto de **Exclusão Lógica** (Soft Delete) e **Auditoria de Dados** (Audit Log) utilizando Python e SQLAlchemy 2.0.

Este módulo resolve dois problemas críticos em sistemas corporativos:
1.  **Prevenção de Perda de Dados:** Registros nunca são removidos fisicamente (`DELETE`), apenas marcados como deletados.
2.  **Rastreabilidade (Compliance):** Todas as alterações de estado (`INSERT`, `UPDATE`, `SOFT_DELETE`) são registradas automaticamente em uma tabela de histórico.

## 🚀 Funcionalidades

### 1. Soft Delete Transparente
* **Mixin Reutilizável:** Adiciona `is_deleted` e `deleted_at` a qualquer tabela.
* **Global Query Filter:** O interceptador `do_orm_execute` injeta automaticamente a cláusula `WHERE is_deleted = False` em todas as consultas `SELECT`.
* **Modo Admin:** Possibilidade de ignorar o filtro via `execution_options(include_deleted=True)`.

### 2. Auditoria Automática (CDC)
* **Event Listeners:** Utiliza o gancho `before_flush` do SQLAlchemy para inspecionar mudanças na sessão antes do commit.
* **Diff de Alterações:** Calcula o "Antes" e "Depois" de cada campo alterado.
* **JSON Storage:** Armazena o snapshot das mudanças em formato JSON, com suporte a serialização de datas (`datetime`).

## 🛠️ Tecnologias

* **Python 3.11+**
* **SQLAlchemy 2.0+** (Modern ORM style)
* **SQLite** (Memória para testes rápidos) / **PostgreSQL** (Produção)
* **Docker & Docker Compose**
* **Pytest** (Testes automatizados)

## 📂 Estrutura do Projeto

```text
src/
├── core.py      # Configuração do ORM, Mixins e Filtro Global
├── models.py    # Definição das tabelas (BankAccount, AuditLog)
└── auditor.py   # Lógica de interceptação e geração de logs (Event Listener)
tests/
├── test_soft_delete.py  # Valida fluxo de deleção e recuperação
└── test_audit.py        # Valida geração de logs de INSERT/UPDATE
```
## ⚡ Como Executar
1. Instalação
```bash
make install
# ou
pip install -r requirements.txt
```
## 2. Rodar Testes
Executa a suíte de testes que valida o Soft Delete e a Auditoria.
```bash
make test
```
## 3. Verificação de Qualidade
```bash
make lint
```
##
🔍 Detalhes de Implementação
O Interceptador de Consultas

Para garantir que dados deletados não vazem na aplicação, usamos with_loader_criteria:
```py
@event.listens_for(Session, "do_orm_execute")
def add_filtering_criteria(execute_state: ORMExecuteState):
    # ... lógica que injeta WHERE is_deleted = False ...
```
O Auditor

O auditor detecta mudanças no flush e gera registros na tabela audit_logs:
```py
// Exemplo de Log gerado
{
  "action": "UPDATE",
  "table": "bank_accounts",
  "old_values": { "balance": 1000.0 },
  "new_values": { "balance": 2500.0 }
}
```

