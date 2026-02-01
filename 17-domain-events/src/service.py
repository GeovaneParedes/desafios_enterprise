from src.bus import EventBus
from src.events import UserRegistered

class UserService:
    def __init__(self, event_bus: EventBus):
        self.bus = event_bus
        self.next_id = 1

    def register_user(self, username: str, email: str):
        # 1. Lógica de Negócio (Core)
        print(f"\n💾 [DB] Salvando usuário '{username}' no banco de dados...")
        user_id = self.next_id
        self.next_id += 1
        
        # 2. Criação do Fato (Evento)
        event = UserRegistered(
            user_id=user_id, 
            username=username, 
            email=email
        )

        # 3. Publicação (Side Effects desacoplados)
        self.bus.publish(event)
        
        return user_id
