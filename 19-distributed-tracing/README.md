# Day 19: Distributed Tracing (OpenTelemetry + Jaeger)

Implementação de **Observabilidade** completa utilizando o padrão **OpenTelemetry (OTel)** para instrumentação e **Jaeger** para visualização de traces.

O Distributed Tracing permite visualizar a jornada de uma requisição através de múltiplos serviços e componentes, identificando gargalos de performance (Bottlenecks) com precisão cirúrgica.

## 🚀 Funcionalidades

### 1. Auto-Instrumentação
* Utiliza bibliotecas do OpenTelemetry para interceptar automaticamente chamadas HTTP (Flask) e comandos de banco de dados (Redis).
* Gera **Spans** (blocos de tempo) sem necessidade de alterar a lógica de negócio.

### 2. Spans Manuais
* Demonstração de como criar spans customizados (`with tracer.start_as_current_span`) para medir funções internas específicas (`validate_user_logic`, `payment_gateway_call`).

### 3. Visualização em Waterfall (Jaeger)
* Interface gráfica para analisar a latência de cada etapa.
* Permite diferenciar tempo de processamento (CPU Bound) de tempo de espera (IO Bound/Network Latency).

## 🛠️ Tecnologias

* **Python 3.11+**
* **OpenTelemetry** (Padrão da indústria para coleta de telemetria)
* **Jaeger** (Backend de armazenamento e UI de traces)
* **Docker** (Infraestrutura do Jaeger all-in-one)

## 📂 Estrutura do Projeto

```text
src/
├── app.py         # Aplicação instrumentada com OTel
└── traffic.py     # Script gerador de tráfego para popular o Jaeger
docker-compose.yml # Container do Jaeger (Portas 16686 UI, 4317 OTLP)
```

## ⚡ Como Executar

## 1. Infraestrutura

Inicia o Jaeger e o Redis.
```bash
make up
```
* Acesse a UI: http://localhost:16686

## 2. Rodar Aplicação
```bash
make run
```
## 3. Gerar Tráfego
```bash
python3 src/traffic.py
```

