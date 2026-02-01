from unittest.mock import MagicMock
from src.bus import EventBus
from src.events import UserRegistered
from src.service import UserService


def test_event_dispatching():
    """Verifica se o listener é chamado quando o serviço roda."""
    # Arrange
    bus = EventBus()
    mock_listener = MagicMock()

    mock_listener.__name__ = "MockListener"

    bus.subscribe(UserRegistered, mock_listener)
    service = UserService(bus)

    # Act
    service.register_user("tester", "test@test.com")

    # Assert
    # O listener foi chamado?
    mock_listener.assert_called_once()

    # O evento passado estava correto?
    args, _ = mock_listener.call_args
    event = args[0]
    assert isinstance(event, UserRegistered)
    assert event.username == "tester"
