import json
import uuid

import requests

# URL da nossa API
URL = "http://localhost:8000/api/v1/payment"


def run_test():
    print("--- 💳 Iniciando Teste de Idempotência Financeira ---")

    # 1. Gera uma chave única para esta tentativa de pagamento
    # O app do cliente geraria isso antes de tentar o primeiro envio.
    idempotency_key = str(uuid.uuid4())
    print(f"🔑 Chave de Idempotência Gerada: {idempotency_key}")

    payload = {"user_id": "user_123_senior", "amount": 150.00}

    headers = {
        "Idempotency-Key": idempotency_key,
        "Content-Type": "application/json",
    }

    # --- TENTATIVA 1: O Pagamento Real ---
    print("\n[1] Enviando PRIMEIRA requisição (Processamento Real)...")
    resp1 = requests.post(URL, json=payload, headers=headers)

    if resp1.status_code != 200:
        print("❌ Falha na primeira requisição!")
        return

    data1 = resp1.json()
    print(f"✅ Sucesso! TX ID: {data1['transaction_id']}")
    print(f"   Mensagem: {data1['message']}")

    # --- TENTATIVA 2: O Retry (Simulando erro de rede) ---
    print(
        "\n[2] Enviando SEGUNDA requisição "
        "(Simulação de Retry com MESMA chave)..."
    )
    print("   ...Aguardando resposta do cache...")
    resp2 = requests.post(URL, json=payload, headers=headers)

    data2 = resp2.json()
    print(f"✅ Resposta recebida! TX ID: {data2['transaction_id']}")
    print(f"   Mensagem: {data2['message']}")

    # --- VALIDAÇÃO FINAL (A Mágica) ---
    print("\n--- 🔍 Análise de Engenharia ---")

    # Valida se os IDs de transação são IDÊNTICOS
    if data1["transaction_id"] == data2["transaction_id"]:
        print("✅ SUCESSO TOTAL: Os IDs de transação são IGUAIS.")
        print(
            "🚀 O sistema identificou a duplicidade e "
            "retornou o recibo antigo."
        )
        print("💰 O cliente NÃO foi cobrado duas vezes.")
    else:
        print("❌ FALHA CRÍTICA: Os IDs são diferentes!")
        print("💸 O cliente foi cobrado duas vezes (R$ 300,00 total).")


if __name__ == "__main__":
    run_test()
