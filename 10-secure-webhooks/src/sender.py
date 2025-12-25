import requests
import json
from src.security import WebhookSecurity

TARGET_URL = "http://localhost:5000/webhook"
SHARED_SECRET = "minha_chave_super_secreta_de_producao"
HACKER_SECRET = "chave_errada_do_hacker"


def send_notification(payload_dict, secret, description):
    payload_str = json.dumps(payload_dict)

    # Gera assinatura
    signature = WebhookSecurity.sign_payload(secret, payload_str)

    headers = {
        "Content-Type": "application/json",
        "X-Hub-Signature-256": signature
    }

    print(f"\n--- Enviando: {description} ---")
    try:
        response = requests.post(TARGET_URL, data=payload_str, headers=headers)
        if response.status_code == 200:
            print(f"✅ {response.status_code}: Aceito pelo servidor.")
        else:
            print(f"❌ {response.status_code}: Rejeitado pelo servidor.")
    except Exception as e:
        print(f"⚠️ Erro de conexão (O servidor está rodando?): {e}")


if __name__ == "__main__":
    # Cenário 1: Requisição Legítima (Chave correta)
    send_notification(
        {"event": "payment_approved", "amount": 500},
        SHARED_SECRET,
        "Pagamento Legítimo"
    )

    # Cenário 2: Ataque Hacker (Chave errada)
    send_notification(
        {"event": "payment_approved", "amount": 999999},
        HACKER_SECRET,
        "Ataque com Chave Falsa"
    )

    # Cenário 3: Man-in-the-Middle (Alterou o payload mas manteve a assinatura
    # original)
    # Isso simula alguém interceptando o pacote e mudando o valor
    print("\n--- Enviando: Ataque de Adulteração ---")
    payload_original = json.dumps({"event": "payment_approved", "amount": 500})
    signature_original = WebhookSecurity.sign_payload(
                SHARED_SECRET,
                payload_original)

    # Hacker muda o valor para 100, mas usa a assinatura do 500
    payload_adulterado = json.dumps(
        {"event": "payment_approved", "amount": 100})

    headers = {
        "Content-Type": "application/json",
        "X-Hub-Signature-256": signature_original
    }
    resp = requests.post(TARGET_URL, data=payload_adulterado, headers=headers)
    print(f"❌ {resp.status_code}: {resp.text}")
