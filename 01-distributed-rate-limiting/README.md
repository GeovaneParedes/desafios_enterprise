# Desafio Enterprise #01: Distributed Rate Limiter

## O Problema (Business Case)
Em sistemas de alta escala, APIs públicas estão sujeitas a picos de tráfego (flash crowds) ou ataques maliciosos (DDoS). Sem controle, um único cliente pode monopolizar os recursos do servidor, causando negação de serviço para todos os outros usuários e aumentando custos de infraestrutura.

## A Solução Técnica
Implementação de um **Rate Limiter Distribuído** utilizando o algoritmo **Sliding Window** (Janela Deslizante).
Diferente de soluções simples em memória (que não funcionam em arquiteturas de múltiplos containers/pods), esta solução utiliza **Redis** para manter o estado global dos contadores.

### Destaques da Implementação
- **Algoritmo:** Sliding Window (mais preciso que Fixed Window).
- **Concorrência:** Uso de operações atômicas no Redis (Lua Script/Pipeline) para evitar Race Conditions.
- **Stack:** Python (FastAPI) + Redis.
- **Design:** Middleware plugável.

---

### A Implementação (Código Sênior)

Vamos usar Python (FastAPI) e Redis. A chave aqui é a eficiência: checar o limite não pode adicionar latência significativa.

## Pré-requisitos:

    Docker (para rodar o Redis)

    Python 3.10+
