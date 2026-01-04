from src.manager import FeatureManager


def run_simulation():
    manager = FeatureManager("flags.json")

    print("--- 🔧 Carregando Feature Flags ---")

    # Cenário 1: Boolean (Maintenance Banner)
    # Está 'enabled: false' no JSON
    if manager.is_enabled("maintenance_banner"):
        print("🔴 BANNER: Sistema em manutenção!")
    else:
        print("🟢 BANNER: Sistema operando normalmente.")

    # Cenário 2: User Targeting (Dark Mode)
    # Permitido apenas para 'user_123' e 'admin_01'
    users = ["user_123", "guest_555", "admin_01"]
    print("\n--- 🌙 Testando Dark Mode (Targeting) ---")
    for u in users:
        status = "ATIVO" if manager.is_enabled(
            "dark_mode_beta", u) else "Inativo"
        print(f"Usuário {u}: {status}")

    # Cenário 3: Percentage Rollout (New Checkout)
    # Configurado para 20%
    print("\n--- 🛒 Testando Novo Checkout (20% Rollout) ---")
    active_count = 0
    total_users = 20

    for i in range(total_users):
        uid = f"customer_{i}"
        if manager.is_enabled("new_checkout_flow", uid):
            print(f"✅ {uid} vê o Novo Checkout")
            active_count += 1
        else:
            print(f"❌ {uid} vê o Checkout Antigo")

    print(f"\nEstatística: {active_count}/{total_users}"
          f"usuários selecionados (Esperado ~20%)")


if __name__ == "__main__":
    run_simulation()
