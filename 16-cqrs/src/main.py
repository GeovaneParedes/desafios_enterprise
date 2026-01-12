from src.handlers import CommandHandler, QueryHandler, CreateUserCommand


def run_cqrs_demo():
    cmd_handler = CommandHandler()
    query_handler = QueryHandler()

    print("--- ✍️ COMMAND: Criando Usuário (Write Side) ---")
    command = CreateUserCommand("devgege", "gege@dev.com", "secret123")
    user_id = cmd_handler.handle_create_user(command)
    print(f"✅ Usuário criado com ID: {user_id}")
    print("(Dados salvos no SQLite com senha hasheada)")

    print("\n--- 👓 QUERY: Lendo Usuário (Read Side) ---")
    user_dto = query_handler.get_user_summary(user_id)
    print(f"Resultado da Query: {user_dto}")
    
    print("\n🔍 Verificando Segregação:")
    if "password_hash" not in user_dto:
        print("✅ Sucesso: A senha não vazou para o modelo de leitura!")
    else:
        print("❌ Falha: A senha vazou!")

    if user_dto["display_name"] == "DEVGEGE":
        print("✅ Sucesso: O modelo de leitura já veio formatado (UPPERCASE).")


if __name__ == "__main__":
    run_cqrs_demo()
