# Day 15: Circuit Breaker Pattern

Implementação de uma máquina de estados para **Proteção de Resiliência** em sistemas distribuídos.

O padrão Circuit Breaker previne **Falhas em Cascata** (Cascading Failures). Quando um serviço externo começa a falhar repetidamente, o "disjuntor" abre, interrompendo imediatamente novas chamadas para evitar sobrecarga e dar tempo de recuperação ao sistema falho.

## 🚀 Funcionalidades

### 1. Máquina de Estados
* **CLOSED (Fechado):** O fluxo flui normalmente. Monitora falhas.
* **OPEN (Aberto):** Bloqueio imediato (Fail Fast). Lança exceção sem executar a chamada real.
* **HALF-OPEN (Meio-Aberto):** Após um tempo de recuperação (`recovery_timeout`), permite uma chamada de teste. Se sucesso → Fecha; Se falha → Abre novamente.

### 2. Fail Fast
* Impede que threads fiquem travadas esperando *timeout* de serviços mortos.
* Retorna erro instantâneo (`CircuitBreakerOpenException`), liberando recursos da aplicação.

### 3. Auto-Recuperação (Self-Healing)
* O sistema tenta voltar ao normal automaticamente assim que o serviço externo estabiliza, sem necessidade de restart manual.

## 🛠️ Tecnologias

* **Python 3.11+**
* **Loguru** (Visualização clara das transições de estado nos logs)
* **Pytest** (Validação da lógica de transição de estados)

## 📂 Estrutura do Projeto

```text
src/
├── circuit.py     # Lógica do Circuit Breaker (States, Thresholds, Timeouts)
├── service.py     # Simulação de serviço instável (Chaos Engineering)
└── main.py        # Demo visual do ciclo de vida (Closed -> Open -> Half-Open)
tests/
└── test_circuit.py # Testes unitários da máquina de estados
```
## ⚡ Como Executar

## 1. Instalação
```bash
make install
```
## 2. Simulação Visual

Observe o comportamento do sistema quando o serviço de pagamento começa a falhar.
```bash
make run
```
## 3. Testes Automatizados
```bash
make test
```

