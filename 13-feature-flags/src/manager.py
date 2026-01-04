import json
import os
from typing import Optional
from src.strategies import Strategies


class FeatureManager:
    def __init__(self, config_path: str = "flags.json"):
        self.config_path = config_path
        self._flags = {}
        self.refresh()

    def refresh(self):
        """Recarrega as configurações do arquivo JSON
        (Simula runtime update).
        """
        if not os.path.exists(self.config_path):
            self._flags = {}
            return

        with open(self.config_path, 'r') as f:
            self._flags = json.load(f)

    def is_enabled(self,
                   feature_name: str,
                   user_id: Optional[str] = None) -> bool:
        """
        Avalia se uma feature está ativa para determinado contexto.
        """
        feature = self._flags.get(feature_name)

        # 1. Feature não existe ou está desabilitada globalmente
        if not feature or not feature.get("enabled", False):
            return False

        # 2. Seleciona a estratégia
        strategy_name = feature.get("strategy", "boolean")
        params = feature.get("parameters", {})

        # 3. Executa a lógica da estratégia
        strategy_fn = getattr(Strategies, strategy_name, Strategies.boolean)

        return strategy_fn(params, user_id)
