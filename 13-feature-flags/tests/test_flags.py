import pytest
from src.strategies import Strategies
from src.manager import FeatureManager


class TestStrategies:
    def test_user_list_strategy(self):
        params = {"users": ["alice", "bob"]}

        assert Strategies.user_list(params, "alice") is True
        assert Strategies.user_list(params, "bob") is True
        assert Strategies.user_list(params, "charlie") is False

    def test_percentage_strategy_deterministic(self):
        """O mesmo usuário deve ter sempre o mesmo resultado para a
        mesma flag.
        """
        params = {"percentage": 50}
        user = "test_user_unique"

        result1 = Strategies.percentage(params, user)
        result2 = Strategies.percentage(params, user)

        assert result1 == result2

    def test_percentage_distribution(self):
        """Verifica se aproxima da porcentagem desejada em grande volume."""
        params = {"percentage": 20}
        total = 1000
        active = 0

        for i in range(total):
            if Strategies.percentage(params, f"user_{i}"):
                active += 1

        # Aceitamos margem de erro estatística
        assert 150 < active < 250  # Entre 15% e 25%


class TestManager:
    def test_feature_disabled_returns_false(self, tmp_path):
        # Cria arquivo de config temporário
        config_file = tmp_path / "test_flags.json"
        config_file.write_text('{"feature_x": {"enabled": false}}')

        manager = FeatureManager(str(config_file))
        assert manager.is_enabled("feature_x") is False

    def test_feature_missing_returns_false(self, tmp_path):
        config_file = tmp_path / "test_flags.json"
        config_file.write_text('{}')

        manager = FeatureManager(str(config_file))
        assert manager.is_enabled("non_existent_feature") is False
