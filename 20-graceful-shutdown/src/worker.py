import time
from loguru import logger
from src.killer import GracefulKiller


def simulate_heavy_task(task_id):
    """
    Simula um trabalho demorado (ex: processar vídeo, relatório, pagamento)"""
    logger.info(f"🔨 [Task {task_id}] Iniciando processamento (5s)...")

    # Simulamos passos do processamento para mostrar que ele não é interrompido
    for i in range(1, 6):
        time.sleep(1)
        # logger.debug(f"   [Task {task_id}] Passo {i}/5 concluído.")

    logger.success(f"✅ [Task {task_id}] Finalizada com sucesso.")


def run_worker():
    killer = GracefulKiller()
    task_id = 1

    logger.info("🚀 Worker iniciado. Pressione Ctrl+C para testar o Shutdown.")

    # Loop Infinito de Trabalho
    while not killer.kill_now:

        # 1. Simula pegar trabalho da fila
        simulate_heavy_task(task_id)
        task_id += 1

        # 2. Simula pequena pausa entre jobs
        # Se o sinal chegar aqui, o killer.kill_now vira True e o loop quebra
        # na próxima verificação
        time.sleep(0.5)

    # Pós-Loop (Cleanup)
    logger.info("🧹 Fechando conexões com banco de dados...")
    time.sleep(1)  # Simula fechar conexões
    logger.info("👋 Shutdown completo. Até logo!")


if __name__ == '__main__':
    run_worker()
