import logging
from flask import Flask, request, jsonify, abort
from src.security import WebhookSecurity

# Configuração
app = Flask(__name__)
SECRET_KEY = "minha_chave_super_secreta_de_producao"

# Configura logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebhookReceiver")


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Endpoint que recebe notificações de terceiros.
    """
    # 1. Capturar o Header de Assinatura
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        logger.warning("⛔ Rejeitado: Header de assinatura ausente.")
        abort(401, description="Missing Signature Header")

    # 2. Capturar o corpo BRUTO (Raw Bytes)
    # É crucial pegar os bytes exatos. Se parsear JSON antes,
    # os espaços em branco podem mudar e invalidar o hash.
    payload = request.get_data()

    # 3. Validar Integridade e Autenticidade
    is_valid = WebhookSecurity.verify_signature(SECRET_KEY, payload, signature)

    if not is_valid:
        logger.error(
            f"⛔ Rejeitado: Assinatura inválida! Recebido: {signature}")
        abort(403, description="Invalid Signature")

    # 4. Processar Negócio (Só chega aqui se for autêntico)
    data = request.json
    logger.info(f"✅ Sucesso! Evento processado: {data}")

    return jsonify({"status": "received", "event": data.get("event")}), 200


if __name__ == '__main__':
    print("🚀 Servidor Webhook rodando na porta 5000...")
    print(f"🔑 Segredo esperado: {SECRET_KEY}")
    app.run(port=5000, debug=True)
