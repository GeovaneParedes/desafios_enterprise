from src.bus import EventBus
from src.events import UserRegistered
from src.listeners import (
    send_welcome_email,
    update_analytics_dashboard,
    notify_sales_team)
from src.service import UserService


def run_domain_events_demo():
    # 1. Setup da Infraestrutura (Wiring)
    bus = EventBus()

    # 2. Registro dos Ouvintes (Configuration)
    # Decidimos aqui quem ouve o quê, não dentro do Service!
    bus.subscribe(UserRegistered, send_welcome_email)
    bus.subscribe(UserRegistered, update_analytics_dashboard)
    bus.subscribe(UserRegistered, notify_sales_team)

    # 3. Execução da Lógica
    service = UserService(bus)

    print("--- Cenário 1: Usuário Comum ---")
    service.register_user("devgege", "gege@gmail.com")

    print("\n--- Cenário 2: Usuário Corporativo (Deve acionar Sales) ---")
    service.register_user("cto_bigcompany", "boss@enterprise.com")


if __name__ == "__main__":
    run_domain_events_demo()
