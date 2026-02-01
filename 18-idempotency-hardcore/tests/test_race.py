import pytest
import threading
import requests
import uuid
import time

BASE_URL = "http://localhost:5000/process-payment"

def make_request(idem_key, results):
    """Função auxiliar para rodar em thread"""
    try:
        resp = requests.post(BASE_URL, headers={"Idempotency-Key": idem_key})
        results.append(resp.status_code)
    except Exception as e:
        results.append(f"Error: {e}")

def test_race_condition_protection():
    """
    Lança 2 requisições SIMULTÂNEAS com a mesma chave.
    - Uma deve ganhar (200 OK)
    - A outra deve bater no Lock (409 Conflict)
    """
    # Importante: O servidor precisa estar rodando em outro terminal (make run)
    # ou podemos usar o client do Flask, mas requests real é mais fiel para threads.
    
    key = str(uuid.uuid4())
    results = []
    
    t1 = threading.Thread(target=make_request, args=(key, results))
    t2 = threading.Thread(target=make_request, args=(key, results))
    
    print("\n🔫 Disparando Thread 1 e Thread 2 simultaneamente...")
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print(f"📊 Resultados: {results}")
    
    # Validação
    assert 200 in results, "Pelo menos uma requisição deveria ter sucesso"
    assert 409 in results, "A requisição concorrente deveria ter sido bloqueada (Lock)"
    assert len(results) == 2

def test_cache_hit_after_completion():
    """
    Após o lock ser liberado e o valor salvo, deve retornar 200 (Cache).
    """
    key = str(uuid.uuid4())
    
    # 1. Primeira chamada (Lenta)
    print("\n🐢 Req 1 (Cold)...")
    resp1 = requests.post(BASE_URL, headers={"Idempotency-Key": key})
    assert resp1.status_code == 200
    
    # 2. Segunda chamada (Imediata)
    print("🐇 Req 2 (Cached)...")
    start = time.time()
    resp2 = requests.post(BASE_URL, headers={"Idempotency-Key": key})
    duration = time.time() - start
    
    assert resp2.status_code == 200
    assert duration < 0.1 # Deve ser instantâneo (sem sleep de 2s)
