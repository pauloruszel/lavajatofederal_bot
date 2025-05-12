import time
from datetime import datetime
from bot_lavajato import main
from logger_config import setup_logging

logger = setup_logging()

def loop_infinito():
    logger.info("🚀 Executor iniciado. Rodando de 30 em 30 minutos, seg a sáb, das 08h às 18h (BRT)")
    while True:
        now = datetime.now()
        hora = now.hour
        dia_semana = now.weekday()  # 0 = segunda, 6 = domingo

        if dia_semana < 6 and 8 <= hora <= 18:
            logger.info("⏳ Executando ciclo de verificação...")
            try:
                main()
                logger.info("✅ Ciclo finalizado com sucesso.")
            except Exception:
                logger.exception("❌ Erro ao executar o ciclo")
        else:
            logger.info("⏸️ Fora do horário comercial. Aguardando próximo ciclo.")

        time.sleep(60 * 30)  # Espera 30 minutos

if __name__ == "__main__":
    loop_infinito()