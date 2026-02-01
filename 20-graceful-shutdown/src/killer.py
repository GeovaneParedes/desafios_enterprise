import signal
from loguru import logger


class GracefulKiller:
    """
    Monitora sinais do sistema operacional (SIGINT, SIGTERM).
    Funciona como uma flag global para a aplicação saber quando deve parar.
    """
    kill_now = False

    def __init__(self):
        # Mapeia os sinais para o método exit_gracefully
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        """
        Callback chamado quando o SO envia um sinal de término.
        """
        signal_name = "SIGINT (Ctrl+C)" if signum == signal.SIGINT else "SIGTERM"  # noqa
        logger.warning(f"\n🛑 Sinal recebido: {signal_name}")
        logger.info("⏳ Iniciando procedimento de Graceful Shutdown...")
        logger.info("   - Não aceitando novos trabalhos.")
        logger.info("   - Aguardando término da tarefa atual...")

        self.kill_now = True
