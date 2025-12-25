import hmac
import hashlib
from typing import Union


class WebhookSecurity:
    """
    Gerencia a assinatura e verificação de payloads de Webhook
    utilizando HMAC-SHA256.
    """

    @staticmethod
    def sign_payload(secret: str, payload: Union[str, bytes]) -> str:
        """
        Gera a assinatura HMAC-SHA256 para um payload.

        Args:
            secret: Chave secreta compartilhada.
            payload: Corpo da requisição (raw bytes ou string).

        Returns:
            String hexadeciaml da assinatura (ex: 'a1b2c3...').
        """
        if isinstance(payload, str):
            payload = payload.encode('utf-8')

        if isinstance(secret, str):
            secret = secret.encode('utf-8')

        # Cria o hash usando o algoritmo SHA256
        signature = hmac.new(
            key=secret,
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()

        return signature

    @staticmethod
    def verify_signature(secret: str, payload: Union[str, bytes],
                         received_signature: str) -> bool:
        """
        Verifica se a assinatura recebida bate com o payload.

        IMPORTANTE: Usa compare_digest para evitar Timing Attacks.
        A comparação comum (==) retorna mais rápido se o início da string
        for diferente, permitindo que atacantes descubram a chave por
        tentativa e erro.
        """
        expected_signature = WebhookSecurity.sign_payload(secret, payload)

        # compare_digest leva o mesmo tempo independente do conteúdo
        return hmac.compare_digest(expected_signature, received_signature)
