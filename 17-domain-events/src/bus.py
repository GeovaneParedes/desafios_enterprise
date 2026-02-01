from typing import Dict, List, Type, Callable, Any
from dataclasses import dataclass


@dataclass
class DomainEvent:
    """Classe base para todos os eventos."""
    pass


# Definição de tipo para um Handler (Função que recebe um evento)
EventHandler = Callable[[Any], None]


class EventBus:
    def __init__(self):
        # Mapeia: TipoDoEvento -> Lista de Funções Ouvintes
        self._subscribers: Dict[Type[DomainEvent], List[EventHandler]] = {}

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler):
        """Registra um ouvinte para um tipo específico de evento."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        print(f"👂 Handler '{handler.__name__}' inscrito em"
              f"{event_type.__name__}")

    def publish(self, event: DomainEvent):
        """Dispara o evento para todos os ouvintes registrados."""
        event_type = type(event)
        handlers = self._subscribers.get(event_type, [])

        if not handlers:
            print(f"⚠️ Nenhum ouvinte para {event_type.__name__}")
            return

        print(f"📣 Publicando {event_type.__name__} para"
              f"{len(handlers)} ouvintes...")
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                # Importante: Um listener não pode quebrar o fluxo
                # principal em eventos síncronos!
                print(f"❌ Erro no handler {handler.__name__}: {e}")
