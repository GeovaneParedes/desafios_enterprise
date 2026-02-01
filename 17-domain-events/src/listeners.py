from src.events import UserRegistered


def send_welcome_email(event: UserRegistered):
    """Simula envio de e-mail (Ex: SendGrid/SES)"""
    print(f"   📧 [EmailService] Enviando 'Bem-vindo"
          f"{event.username}' para {event.email}...")


def update_analytics_dashboard(event: UserRegistered):
    """Simula atualização de KPI (Ex: Google Analytics/Mixpanel)"""
    print(f"   📊 [Analytics] Incrementando métrica 'daily_signups'"
          f"(User ID: {event.user_id}).")


def notify_sales_team(event: UserRegistered):
    """Simula notificação no Slack"""
    if "enterprise" in event.email:
        print(f"   💰 [Sales] LEAD IMPORTANTE DETECTADO: {event.email}!")
