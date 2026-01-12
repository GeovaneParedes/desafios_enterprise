from typing import Dict, Any, Optional


class UserReadDB:
    """
    Simula um banco NoSQL otimizado para leitura.
    Armazena apenas dados desnormalizados (DTOs).
    """
    _storage: Dict[int, Dict[str, Any]] = {}

    @classmethod
    def save(cls, user_id: int, data: Dict[str, Any]):
        cls._storage[user_id] = data

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[Dict[str, Any]]:
        return cls._storage.get(user_id)

    @classmethod
    def get_all(cls) -> list:
        return list(cls._storage.values())
