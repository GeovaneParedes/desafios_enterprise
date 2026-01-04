# Day 14: API Rate Limiting (Redis)

Implementação de um mecanismo de **Rate Limiting** distribuído utilizando Redis e o algoritmo de **Janela Fixa (Fixed Window)**.

Este padrão protege a API contra abuso (DDoS, Brute Force ou scripts mal configurados), limitando o número de requisições que um cliente pode fazer em um determinado período de tempo.

## 🚀 Funcionalidades

### 1. Algoritmo Fixed Window
* Conta requisições baseando-se em janelas de tempo discretas (ex: 10:00:00 a 10:00:59).
* Utiliza a fórmula `Timestamp / Janela` para gerar chaves de tempo únicas.

### 2. Contadores Atômicos (Redis)
* Utiliza o comando `INCR` do Redis para garantir contagem precisa mesmo em ambientes concorrentes/distribuídos.
* Utiliza `EXPIRE` para limpar automaticamente chaves antigas, evitando vazamento de memória.

### 3. Fail-Fast
* Se o limite é excedido, o sistema retorna imediatamente `False` (simulando um HTTP 429 Too Many Requests), poupando recursos de processamento da aplicação.

## 🛠️ Tecnologias

* **Python 3.11+**
* **Redis 7** (Armazenamento em memória de alta performance)
* **Docker Compose** (Infraestrutura do Redis)
* **Pytest** (Testes de integração)

## 📂 Estrutura do Projeto

```text
src/
├── limiter.py     # Lógica do Rate Limiter (Redis INCR + EXPIRE)
└── main.py        # Simulação de tráfego e bloqueio
tests/
└── test_limiter.py # Testes de validação de bloqueio e reset de janela
docker-compose.yml  # Definição do serviço Redis
```
## ⚡ Como Executar
## 1. Subir Infraestrutura

```bash
make up
```
## 2. Instalar Dependências
```bash
make install
```
## 3. Simulação Visual

Tenta realizar 10 requisições seguidas (Regra: 5 reqs/10s).
```bash
make run
```
## 4. Rodar Testes
```bash
make test
```

