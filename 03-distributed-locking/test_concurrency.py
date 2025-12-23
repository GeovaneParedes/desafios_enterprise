import concurrent.futures
import requests
import time

URL = "http://localhost:8000/comprar"

def tentar_comprar(user_id):
    try:
        response = requests.post(URL, json={"user_id": f"user_{user_id}"})
        return response.status_code, response.json()
    except Exception as e:
        return 500, str(e)

def run_stress_test():
    print("--- 🎫 INICIANDO TESTE DE CONCORRÊNCIA (BLACK FRIDAY) ---")
    print("Objetivo: 20 usuários tentando comprar 1 único ingresso simultaneamente.\n")

    # Número de usuários simultâneos
    n_users = 20
    
    sucessos = 0
    falhas = 0
    esgotados = 0

    # Dispara as requisições em paralelo (Threads)
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_users) as executor:
        # Cria a lista de tarefas
        futures = [executor.submit(tentar_comprar, i) for i in range(n_users)]
        
        for future in concurrent.futures.as_completed(futures):
            status, data = future.result()
            
            if status == 200:
                print(f"✅ SUCESSO: {data}")
                sucessos += 1
            elif status == 409:
                print(f"❌ ESGOTADO: {data['detail']}")
                esgotados += 1
            else:
                print(f"⚠️ ERRO ({status}): {data}")
                falhas += 1

    print("\n--- 📊 RELATÓRIO FINAL ---")
    print(f"Total Tentativas: {n_users}")
    print(f"Vendas Realizadas: {sucessos} (Esperado: 1)")
    print(f"Barrados (Esgotado): {esgotados}")
    print(f"Erros de Sistema: {falhas}")

    if sucessos == 1:
        print("\n🏆 RESULTADO: LOCK FUNCIONOU! Sistema íntegro.")
    elif sucessos > 1:
        print("\n💀 FALHA GRAVE: OVERBOOKING! Vendeu mais do que tinha.")
    else:
        print("\n❓ ESTRANHO: Ninguém comprou?")

if __name__ == "__main__":
    run_stress_test()
