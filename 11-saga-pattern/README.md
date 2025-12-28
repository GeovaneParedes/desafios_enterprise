# Day 11: Saga Pattern (Orchestration)

Implementação do padrão **Saga** baseada em orquestração para gerenciamento de transações distribuídas.

Em arquiteturas de microsserviços, transações que abrangem múltiplos serviços não podem depender de ACID (Atomicidade, Consistência, Isolamento, Durabilidade) de um único banco de dados. O Saga Pattern garante a **Consistência Eventual** através de ações compensatórias.

## 🚀 Funcionalidades

### 1. Máquina de Estados (Orchestrator)
* Gerencia centralmente a execução de uma sequência de passos (`Steps`).
* Monitora o sucesso ou falha de cada etapa.

### 2. Rollback Automático (Compensação)
* Implementa o padrão **Command/Undo**.
* Se o Passo N falhar, o orquestrador executa o método `compensate()` dos passos N-1, N-2... até o início.
* Garante que o sistema retorne a um estado consistente (ex: estornar pagamento se o envio falhar).

## 🛠️ Tecnologias

* **Python 3.11+**
* **Loguru** (Logging estruturado)
* **Pytest & Unittest.Mock** (Testes de comportamento e interação)

## 📂 Estrutura do Projeto

```text
src/
├── interface.py     # Protocolo abstrato (execute/compensate)
├── orchestrator.py  # Lógica de controle de fluxo e rollback
├── steps.py         # Implementação dos serviços (Stock, Payment, Shipping)
└── main.py          # Simulação de cenários (Sucesso vs Falha)
tests/
└── test_saga.py     # Validação unitária com Mocks
```

## ⚡ Como Executar
1. Instalação
```bash
make install
```

## 2. Executar Simulação Visual

Roda os cenários de "Compra com Sucesso" e "Falha no Pagamento".
```bash
make run
```

## 3. Rodar Testes

Valida a lógica de rollback e ordem de chamadas.
```bash
make test
```
