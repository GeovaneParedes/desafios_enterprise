# Desafio Enterprise #04: Circuit Breaker

## O Problema (Business Case)
Em arquiteturas de microsserviços, a falha de um serviço dependente (ex: Gateway de Pagamento, API de Frete) pode causar **falhas em cascata**.
Se a API de Frete demora 30s para responder (timeout), sua API principal fica travada esperando, consumindo threads e memória, até cair também.

## A Solução Técnica
O padrão **Circuit Breaker** previne que uma aplicação tente executar uma operação que provavelmente falhará.
Ele "abre o circuito" (interrompe o fluxo) após um número de falhas consecutivas, retornando erro imediatamente (**Fail Fast**) e dando tempo para o serviço externo se recuperar.

### Máquina de Estados (Redis)
1.  **CLOSED:** Requisições passam. Conta falhas. Se falhas > Limite -> Muda para OPEN.
2.  **OPEN:** Rejeita requisições imediatamente (HTTP 503). Após tempo X -> Muda para HALF-OPEN (virtualmente).
3.  **HALF-OPEN:** Permite passar 1 teste. Se Sucesso -> CLOSED. Se Falha -> OPEN.

### Como Testar

1.  **Inicie o Redis:**
    ```bash
    docker run -d -p 6379:6379 --name redis-cb redis:alpine
    ```

2.  **Inicie o Serviço Externo (Simulador) em um terminal:**
    ```bash
    make run-external
    # Roda na porta 8001
    ```

3.  **Inicie a API Principal em outro terminal:**
    ```bash
    make run
    # Roda na porta 8000
    ```

4.  **Derrube o Serviço Externo:**
    Faça um POST para `http://localhost:8001/toggle` ou mate o processo do terminal do serviço externo.

5.  **Teste o Disjuntor:**
    Acesse `http://localhost:8000/consultar` várias vezes.
    - As 3 primeiras vão demorar e falhar (Timeout).
    - A 4ª vai falhar **instantaneamente** (Circuit Breaker Open).
