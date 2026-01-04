import hashlib
from typing import Dict, Any, Optional


class Strategies:
    @staticmethod
    def boolean(params: Dict[str, Any], user_id: Optional[str] = None) -> bool:
        """Simplesmente retorna True ou False baseado no status global."""
        return True
        # Se a flag está 'enabled' no JSON e a estratégia é bool, então é True.

    @staticmethod
    def user_list(params: Dict[str,
                  Any], user_id: Optional[str] = None) -> bool:
        """Verifica se o usuário está na lista permitida."""
        if not user_id:
            return False

        allowed_users = params.get("users", [])
        return user_id in allowed_users

    @staticmethod
    def percentage(params: Dict[str,
                   Any], user_id: Optional[str] = None) -> bool:
        """
        Rollout gradual (Canary).
        Usa hash MD5 do user_id para garantir distribuição uniforme e
        determinística.
        """
        if not user_id:
            return False

        percentage = params.get("percentage", 0)

        # Cria um hash numérico do ID do usuário (0-100)
        hash_obj = hashlib.md5(user_id.encode())
        # Pega os primeiros bytes e converte para int
        hash_val = int(hash_obj.hexdigest(), 16)
        # Normaliza para 0-99
        user_score = hash_val % 100

        return user_score < percentage
