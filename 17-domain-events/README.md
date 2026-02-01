# Day 17: Domain Events (Observer Pattern)

Implementação de um **Event Bus** síncrono para aplicar o padrão **Observer** e desacoplar regras de negócio (Core) de efeitos colaterais (Side Effects).

Em vez de um serviço "Deus" que faz tudo (Salva, Envia Email, Notifica Slack, Loga Analytics), o serviço apenas publica um fato: "Isso aconteceu". Os interessados (Listeners) reagem a esse fato.

## 🚀 Funcionalidades

### 1. Desacoplamento (Open/Closed Principle)
* O `UserService` não conhece o `EmailService` nem o `AnalyticsService`.
* Novos comportamentos podem ser adicionados criando novos Listeners, sem tocar no código do serviço principal.

### 2. Event Bus
* Um mediador simples que gerencia inscrições (`subscribe`) e publicações (`publish`).
* Permite múltiplos ouvintes para o mesmo evento.

### 3. Contexto Rico
* O evento `UserRegistered` transporta todos os dados necessários (DTO imutável) para que os ouvintes possam trabalhar sem precisar consultar o banco de dados novamente.

## 🛠️ Tecnologias

* **Python 3.11+**
* **Dataclasses** (Para eventos imutáveis)
* **Pytest & MagicMock** (Para validar se os eventos foram disparados corretamente)

## 📂 Estrutura do Projeto

```text
src/
├── bus.py         # O "Correio" (Gerencia subscribers e publica eventos)
├── events.py      # Definição dos fatos (UserRegistered)
├── listeners.py   # As reações (Email, Analytics, Sales)
├── service.py     # O Emissor (Gera o evento após salvar no DB)
└── main.py        # Configuração (Wiring) e execução
tests/
└── test_events.py # Testes unitários do disparo de eventos
```
## ⚡ Como Executar

## 1. Instalação

```bash
make install
```

## 2. Simulação Visual

Observe como o cadastro de um e-mail corporativo dispara logs adicionais (Sales Team) automaticamente.

```bash
make run
```

## 3. Testes Automatizados

```bash
make test
```

