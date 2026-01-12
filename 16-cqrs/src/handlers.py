from src.write_model import SessionLocal, User
from src.read_model import UserReadDB


class CreateUserCommand:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password


class CommandHandler:
    def handle_create_user(self, command: CreateUserCommand) -> int:
        """
        1. Valida regras de negócio.
        2. Persiste no Write Model (SQL).
        3. Sincroniza com o Read Model (NoSQL).
        """
        session = SessionLocal()

        # --- Write Side ---
        # Simulação de hash de senha
        fake_hash = f"hashed_{command.password}"

        new_user = User(
            username=command.username,
            email=command.email,
            password_hash=fake_hash
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        user_id = new_user.id
        session.close()

        # --- Sync (Projection) ---
        # Projetamos os dados para o formato de leitura.
        # Note que NÃO enviamos o password_hash.
        read_model_data = {
            "id": user_id,
            "display_name": command.username.upper(),  # Ex: lógica de
            "contact": command.email,  # apresentação pré-calculada
        }
        UserReadDB.save(user_id, read_model_data)

        return user_id


class QueryHandler:
    def get_user_summary(self, user_id: int):
        """
        Lê direto do Read Model. Zero processamento, super rápido.
        """
        return UserReadDB.get_by_id(user_id)
