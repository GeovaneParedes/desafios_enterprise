# Desafio 07: Distributed Cache Strategy (Stampede Protection)

Implementação de uma estratégia robusta de cache (*Cache-Aside*) com proteção contra **Cache Stampede** (também conhecido como *Thundering Herd Problem*).

## O Problema

Em sistemas de alta concorrência, quando uma chave de cache muito requisitada expira, múltiplas *threads* ou serviços podem tentar regenerar esse valor simultaneamente. Isso causa:
1.  Pico de carga no Banco de Dados (Database CPU spike).
2.  Latência elevada para todos os usuários.
3.  Desperdício de recursos computacionais (cálculo redundante).

## A Solução

Utilizamos o padrão **Probabilistic Locking** ou **Mutex Distribuído com Double-Check**:

1.  **Leitura Otimista:** Tenta ler do cache.
2.  **Mutex (Lock):** Se falhar (miss), tenta adquirir um lock distribuído no Redis (`SETNX`).
3.  **Double-Check:** Quem adquire o lock verifica o cache novamente (pois outra thread pode ter acabado de escrever).
4.  **Cálculo:** Se ainda vazio, executa a consulta pesada (DB/API).
5.  **Write:** Escreve no cache e libera o lock.
6.  **Backoff:** Quem não consegue o lock espera (sleep exponencial) e tenta ler do cache novamente.

## Estrutura do Projeto

* `src/stampede_guard.py`: Implementação do algoritmo de proteção.
* `src/cache_client.py`: Factory de conexão Redis.
* `tests/integration`: Teste de carga simulando 50 threads concorrentes (Requer Docker).
* `tests/unit`: Testes lógicos usando `fakeredis`.

## Como Executar

### Pré-requisitos
* Docker e Docker Compose
* Python 3.11+

### Comandos
```bash
# Instalar dependências
make install

# Formatar código (Black/Isort 79 chars)
make format

# Rodar todos os testes (Unitários e Integração)
# Nota: Requer docker rodando para integração
docker-compose up -d
make test
docker-compose down
```
