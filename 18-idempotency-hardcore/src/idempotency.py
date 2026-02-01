import json
import redis
from functools import wraps
from flask import request, jsonify, make_response

# Conexão Redis na porta 6381
r = redis.Redis(host='localhost', port=6381, decode_responses=True)

LOCK_VALUE = "IN_PROGRESS"
LOCK_TTL = 30  # Se o servidor morrer processando, libera em 30s
CACHE_TTL = 86400 # Cache do resultado por 24h

def idempotent_hardcore(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('Idempotency-Key')
        
        if not key:
            return f(*args, **kwargs)

        redis_key = f"idem:{key}"

        # --- 1. Tentativa de Bloqueio Atômico (SETNX) ---
        # Tenta escrever "IN_PROGRESS" se e somente se a chave NÃO existir
        acquired_lock = r.set(redis_key, LOCK_VALUE, nx=True, ex=LOCK_TTL)

        if acquired_lock:
            # >>> CENÁRIO 1: Sou o primeiro! (Lock Adquirido) <<<
            print(f"🔓 [LOCK ACQUIRED] Iniciando processamento para {key}")
            try:
                # Executa a função real (pode demorar)
                response = f(*args, **kwargs)
                
                # Normaliza resposta do Flask
                if isinstance(response, tuple):
                    body, status = response
                else:
                    body, status = response.get_json(), response.status_code

                # --- 2. Salva Resultado Final (Substitui o Lock) ---
                payload = json.dumps({"body": body, "status": status})
                # Setex sobrescreve o "IN_PROGRESS"
                r.setex(redis_key, CACHE_TTL, payload)
                print(f"💾 [SAVED] Resultado salvo para {key}")
                
                return body, status

            except Exception as e:
                # Se der erro no código, LIBERA o lock para permitir retry
                print(f"❌ [ERROR] Falha no processamento. Liberando lock.")
                r.delete(redis_key)
                raise e

        else:
            # >>> CENÁRIO 2: Chave já existe (Lock ou Cache) <<<
            stored_value = r.get(redis_key)
            
            # Caso A: Ainda está processando (Race Condition)
            if stored_value == LOCK_VALUE:
                print(f"⛔ [CONFLICT] Requisição concorrente detectada para {key}")
                return jsonify({"error": "Request in progress"}), 409
            
            # Caso B: Já terminou (Retry tardio)
            if stored_value:
                print(f"♻️ [CACHE HIT] Retornando resposta antiga para {key}")
                data = json.loads(stored_value)
                return data['body'], data['status']
            
            # Caso C: Lock expirou bem na hora (Raro, mas possível)
            return jsonify({"error": "Lock state inconsistent, try again"}), 500

    return decorated_function
