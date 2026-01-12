# Day 16: CQRS (Command Query Responsibility Segregation)

Implementação do padrão arquitetural **CQRS**, separando explicitamente os modelos de **Escrita (Write/Command)** e **Leitura (Read/Query)**.

Em sistemas complexos, o modelo de dados ideal para garantir integridade transacional (3ª Forma Normal) raramente é o modelo ideal para consultas de alta performance (Desnormalizado/DTOs). O CQRS resolve isso segregando as responsabilidades.

## 🚀 Funcionalidades

### 1. Write Model (Command Side)
* Focado em regras de negócio e integridade.
* Utiliza **SQLAlchemy** (Relacional) para persistência segura.
* Realiza operações pesadas como Hashing de Senha.

### 2. Read Model (Query Side)
* Focado em performance de leitura e facilidade de consumo pela UI.
* Simula um banco **NoSQL** (Key-Value) em memória.
* Armazena dados já projetados (Ex: `display_name` em uppercase) e seguros (sem campos sensíveis como `password`).

### 3. Sincronização
* O `CommandHandler` atua como orquestrador, salvando no banco de escrita e atualizando a projeção de leitura na mesma operação.

## 🛠️ Tecnologias

* **Python 3.11+**
* **SQLAlchemy** (Write Model)
* **Pytest** (Validação da segregação e projeção de dados)

## 📂 Estrutura do Projeto

```text
src/
├── write_model.py # Definição das tabelas SQL (User com password_hash)
├── read_model.py  # Simulação de NoSQL (Dicionário com DTOs otimizados)
├── handlers.py    # CommandHandler (Regras) e QueryHandler (Leitura)
└── main.py        # Demo da separação de responsabilidades
tests/
└── test_cqrs.py   # Testes garantindo que dados sensíveis não vazam na leitura
```
## ⚡ Como Executar
## 1. Instalação
```bash
make install
```
## 2. Simulação Visual
```bash
make run
```
## 3. Testes Automatizados
```bash
make test
```

