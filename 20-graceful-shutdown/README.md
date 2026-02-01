# Day 20: Graceful Shutdown (SIGTERM Handling)

Implementação de um mecanismo de **Finalização Graciosa** para serviços de backend (Workers/APIs).

Em ambientes orquestrados (Kubernetes/Docker), os processos são frequentemente reiniciados ou movidos. Sem o tratamento adequado de sinais do SO (`SIGTERM`), o encerramento abrupto pode causar perda de dados, corrupção de arquivos e transações incompletas.

## 🚀 Funcionalidades

### 1. Interceptação de Sinais
* A classe `GracefulKiller` monitora os sinais `SIGINT` (Ctrl+C) e `SIGTERM` (Kill/Deploy do K8s).
* Funciona como um **Semáforo Global**, alterando o estado da aplicação de "Rodando" para "Draining" (Esvaziando).

### 2. Proteção de Tarefas em Andamento
* O Worker verifica a flag de desligamento apenas **entre** as tarefas.
* Se um sinal chega **durante** o processamento de uma tarefa crítica, o código garante que ela seja concluída antes de encerrar o processo.

### 3. Cleanup Seguro
* Fecha conexões de banco de dados e libera recursos de forma ordenada antes do `sys.exit(0)`.

## 🛠️ Tecnologias

* **Python 3.11+**
* **Signal Library** (Biblioteca padrão para interação com POSIX signals)
* **Loguru** (Logging para visualizar o fluxo de desligamento)

## 📂 Estrutura do Projeto

```text
src/
├── killer.py      # Gerenciador de Sinais (Signal Handler)
└── worker.py      # Aplicação que processa tarefas longas e respeita o Killer
```
## ⚡ Como Executar

## 1. Instalação
```bash
make install
```
## 2. Rodar Worker
```bash
make run
```
## 3. Testar Shutdown

Enquanto o worker estiver processando uma tarefa (🔨 [Task X]...), pressione Ctrl+C apenas uma vez. Observe que ele não para imediatamente. Ele termina a tarefa atual (✅) e só depois desliga (👋).

* O worker ignorou o instinto de morrer, terminou o trabalho pendente (salvando a integridade dos dados) e só então desligou as luzes. Isso é a diferença entre um sistema amador e um Enterprise.
