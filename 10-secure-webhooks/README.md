# Day 10: Secure Webhooks (HMAC-SHA256)

Implementação de referência para segurança em integração de sistemas via Webhooks.

Este módulo demonstra como garantir **Autenticidade** e **Integridade** em requisições HTTP recebidas de terceiros (como Gateways de Pagamento, GitHub, Slack), utilizando assinaturas digitais HMAC.

## 🚀 Funcionalidades

### 1. Assinatura Digital (HMAC)
* Utiliza o algoritmo **SHA-256** para gerar um hash único do payload combinado com um segredo compartilhado (`Shared Secret`).
* Garante que o remetente é quem diz ser (Autenticação).

### 2. Proteção contra Tampering
* Qualquer alteração no corpo da requisição (ex: mudar `amount: 500` para `amount: 10`) invalida a assinatura.
* O sistema recalcula o hash do payload recebido e compara com o header `X-Hub-Signature-256`.

### 3. Proteção contra Timing Attacks
* Utiliza `hmac.compare_digest` para comparação de strings em tempo constante, prevenindo que atacantes descubram a chave secreta medindo o tempo de resposta da CPU.

## 🛠️ Tecnologias

* **Python 3.11+**
* **Flask** (Servidor Web)
* **HMAC & Hashlib** (Criptografia Padrão)
* **Pytest** (Testes de Segurança e Integração)

## 📂 Estrutura do Projeto

```text
src/
├── security.py  # Core de Criptografia (Geração e Validação de Assinaturas)
├── receiver.py  # Servidor Flask (Valida o Header X-Hub-Signature-256)
└── sender.py    # Script Simulador (Gera requisições legítimas e ataques)
tests/
└── test_webhook.py # Testes automatizados de cenários de ataque e sucesso
```

## ⚡ Como Executar
1. Instalação
```bash
make install
```
## 2. Rodar Servidor (Receiver)

Inicia a API na porta 5000.
```bash
make run-server
```
## 3. Simular Envios (Sender)

Em outro terminal, envia requisições de teste (Legítimas vs Ataques).
```bash
make run-sender
```
## 4. Rodar Testes

Valida a lógica criptográfica e os status HTTP.
```bash
make test
```

