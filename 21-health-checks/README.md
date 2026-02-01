# Day 21: Health Checks (Liveness & Readiness Probes)

Implementação de padrões de **Monitoramento de Saúde** para orquestração de containers (Kubernetes).

Diferenciar "Estar Vivo" (Liveness) de "Estar Pronto" (Readiness) é crucial para evitar loops de reinicialização desnecessários e garantir Zero Downtime durante deploys ou falhas temporárias de dependências.

## 🚀 Funcionalidades

### 1. Liveness Probe (`/health/live`)
* **Pergunta:** "O processo está travado/zumbi?"
* **Ação em Falha:** Reiniciar o Container (Restart).
* **Cenário Simulado:** Deadlock na aplicação. O processo existe, mas não processa nada. O Probe retorna 500 e o orquestrador mata o pod.

### 2. Readiness Probe (`/health/ready`)
* **Pergunta:** "Posso receber tráfego de usuários?"
* **Ação em Falha:** Remover do Load Balancer (Stop Traffic).
* **Cenário Simulado:** Inicialização lenta ou Queda do Banco de Dados. O Probe retorna 503. O container continua rodando (aguardando recuperação), mas nenhum usuário é direcionado para ele.

### 3. Simulador de Kubelet
* Um script Python que atua como o agente do Kubernetes, consultando os endpoints periodicamente e tomando decisões de "Restart" ou "Isolamento de Tráfego" baseadas nos códigos HTTP de retorno.

## 🛠️ Tecnologias

* **Python 3.11+ (Flask)**
* **Requests** (Para simular o agente de monitoramento)
* **Chaos Engineering** (Endpoints `/admin/*` para injetar falhas propositais)

## 📂 Estrutura do Projeto

```text
src/
├── app.py             # Aplicação com endpoints de saúde e injeção de falhas
└── kube_simulator.py  # Script que simula o comportamento do Kubernetes
```
## ⚡ Como Executar

## 1. Instalação
```bash
make install
```
## 2. Rodar a Aplicação (Terminal 1)
```bash
make run-app
```
## 3. Rodar o Simulador (Terminal 2)
```bash
make run-kube
```
## 4. Injetar Caos (Terminal 3)
```bash
# Simular Startup completo (Readiness OK)
curl http://localhost:5000/admin/startup

# Simular Queda do Banco (Readiness Falha, Liveness OK)
curl http://localhost:5000/admin/crash_db

# Simular Travamento Total (Liveness Falha -> Restart)
curl http://localhost:5000/admin/deadlock
```
## Os logs contam a história perfeita de um sistema resiliente:

* Proteção de Startup: O sistema bloqueou tráfego (⛔) até estar pronto. Usuários não viram erros de conexão.

* Proteção de Falha Temporária: Quando o Banco caiu (2º bloco de erros ⛔), o Kubernetes parou de mandar tráfego, mas não matou o pod. Assim que o banco voltasse, o pod estaria pronto instantaneamente.

* Cura de Travamento: Quando ocorreu o Deadlock (3º bloco 💀), aí sim o Kubernetes detectou que o processo era um "zumbi" e decidiu reiniciar.

Você acabou de implementar a lógica que mantém sites gigantes no ar mesmo quando partes da infraestrutura falham. 
Isso é engenharia de software.
