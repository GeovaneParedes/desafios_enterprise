# Desafio Enterprise #02: Idempotency Middleware

## O Problema (Business Case)
Em sistemas financeiros e de pagamentos, a rede não é confiável. Uma requisição de pagamento pode ser processada com sucesso pelo servidor, mas a resposta (ACK) pode se perder antes de chegar ao cliente (timeout).
O cliente, achando que falhou, tenta novamente (Retry).

Sem idempotência, o resultado é catastrófico:
- **Cobrança Dupla:** O cliente é debitado duas vezes.
- **Inconsistência de Dados:** Duplicação de registros no banco.
- **Prejuízo Financeiro:** Custos operacionais com estornos e perda de confiança.

## A Solução Técnica
Implementação de um **Middleware de Idempotência** que intercepta requisições baseadas em uma chave única (`Idempotency-Key`).
Se a chave já foi processada com sucesso anteriormente, o sistema retorna a **resposta cacheada** imediatamente, sem executar a lógica de negócio novamente.

### Arquitetura da Solução
1. **Interceptação:** O Middleware verifica o header `Idempotency-Key` antes da rota.
2. **Atomicidade:** Consulta ao Redis para verificar existência da chave.
3. **Cache de Resposta:** Se a chave existe, retorna o JSON salvo (Status 200).
4. **Processamento:** Se não existe, processa a transação.
5. **Persistência:** Se a transação for sucesso (2xx), salva o resultado no Redis com TTL (Time To Live).

### Destaques da Implementação
- **Performance:** Uso de `ujson` para serialização rápida de payloads.
- **Resiliência:** Tratamento de streams assíncronos (`StreamingResponse`) do FastAPI.
- **Isolamento:** Lógica desacoplada em Middleware (Reutilizável).
- **Stack:** Python 3.10+ (FastAPI), Redis 7.x.

---

## Como Rodar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Docker e Python 3.10+ instalados.

### 2. Configuração do Ambiente
Utilize o `Makefile` para automatizar o setup:

```bash
# Cria o ambiente virtual e instala dependências
python3 -m venv env
source env/bin/activate
make install
