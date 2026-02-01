import time
import redis
import random
from flask import Flask, jsonify

# --- Imports do OpenTelemetry ---
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Instrumentadores Automáticos
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

# 1. Configuração do OTel (Boilerplate padrão)
resource = Resource(attributes={
    "service.name": "payment-service-xray" # Nome que aparecerá no Jaeger
})

tracer_provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True))
tracer_provider.add_span_processor(processor)
trace.set_tracer_provider(tracer_provider)

# 2. Inicializa o App
app = Flask(__name__)

# 3. Ativa Instrumentação Automática!
# Isso faz com que toda requisição HTTP e comando Redis vire um Span.
FlaskInstrumentor().instrument_app(app)
RedisInstrumentor().instrument()

# Setup Redis
r = redis.Redis(host='localhost', port=6382, decode_responses=True)
tracer = trace.get_tracer(__name__)

@app.route('/checkout')
def checkout():
    with tracer.start_as_current_span("checkout_process"):
        # Simulando uma operação complexa
        user_id = f"user_{random.randint(1, 100)}"
        
        # Etapa 1: Validar Usuário (Rápido)
        validate_user(user_id)
        
        # Etapa 2: Buscar Carrinho no Redis (IO Bound)
        cart = get_cart_from_redis(user_id)
        
        # Etapa 3: Processar Pagamento (Lento - CPU Bound simulado)
        process_payment()
        
        return jsonify({"status": "success", "cart": cart})

def validate_user(uid):
    # Criando um Span Manual para uma função interna
    with tracer.start_as_current_span("validate_user_logic"):
        time.sleep(0.05) # Validação rápida
        print(f"Validando {uid}...")

def get_cart_from_redis(uid):
    # O RedisInstrumentor vai criar spans automáticos para os comandos set/get aqui
    r.set(f"cart:{uid}", "iphone_15", ex=60)
    return r.get(f"cart:{uid}")

def process_payment():
    with tracer.start_as_current_span("payment_gateway_call"):
        # Simula lentidão externa
        delay = random.uniform(0.5, 1.5)
        time.sleep(delay)
        print(f"Pagamento processado em {delay:.2f}s")

if __name__ == '__main__':
    print("🔭 Raio-X ligado! Acesse http://localhost:16686 após fazer requisições.")
    app.run(port=5000, debug=True)
