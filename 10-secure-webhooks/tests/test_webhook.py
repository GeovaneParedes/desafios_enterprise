import pytest
import json
from src.security import WebhookSecurity
from src.receiver import app

# Constante usada no receiver.py
SECRET_KEY = "minha_chave_super_secreta_de_producao"


class TestWebhookSecurity:
    """
    Suíte de testes para validação de segurança HMAC e integração HTTP.
    """

    def test_hmac_generation(self):
        """
        Teste Unitário: Valida se a assinatura gerada é determinística.
        """
        payload = '{"test": "data"}'
        signature = WebhookSecurity.sign_payload(SECRET_KEY, payload)

        # O hash deve ser sempre o mesmo para o mesmo input
        assert isinstance(signature, str)
        assert len(signature) == 64  # SHA256 produz 64 caracteres hex
        assert WebhookSecurity.verify_signature(
            SECRET_KEY,
            payload,
            signature) is True

    def test_verify_rejects_tampering(self):
        """
        Teste Unitário: Valida se a verificação falha ao alterar 1 bit do
        payload.
        """
        payload = '{"amount": 100}'
        signature = WebhookSecurity.sign_payload(SECRET_KEY, payload)

        # Altera o payload mas mantém a assinatura original
        fake_payload = '{"amount": 900}'

        is_valid = WebhookSecurity.verify_signature(
            SECRET_KEY,
            fake_payload,
            signature)
        assert is_valid is False


@pytest.fixture
def client():
    """Fixture do Flask para testes de integração."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_webhook_success_flow(client):
    """
    Teste de Integração: Envio correto com Header válido deve retornar 200.
    """
    data = {"event": "ping", "value": 123}
    payload_json = json.dumps(data)

    # Gera assinatura correta
    signature = WebhookSecurity.sign_payload(SECRET_KEY, payload_json)

    response = client.post(
        '/webhook',
        data=payload_json,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature-256": signature
        }
    )

    assert response.status_code == 200
    assert response.json["status"] == "received"


def test_webhook_forbidden_invalid_signature(client):
    """
    Teste de Integração: Assinatura incorreta deve retornar 403.
    """
    data = {"event": "attack"}
    payload_json = json.dumps(data)

    response = client.post(
        '/webhook',
        data=payload_json,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature-256": "assinatura_totalmente_errada"
        }
    )

    assert response.status_code == 403


def test_webhook_unauthorized_missing_header(client):
    """
    Teste de Integração: Falta do header deve retornar 401.
    """
    response = client.post(
        '/webhook',
        json={"event": "oops"},
        # Sem headers
    )

    assert response.status_code == 401
