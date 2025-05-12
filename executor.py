import time
from datetime import datetime
from bot_lavajato import main
from logger_config import setup_logging

logger = setup_logging()

def loop_infinito():
    while True:
        hora = datetime.now().hour
        dia_semana = datetime.now().weekday()  # 0 = segunda, 6 = domingo

        if dia_semana < 6 and 8 <= hora <= 18:
            logger.info("⏳ Executando ciclo de verificação...")
            try:
                main()  # ou outra função sua que cheque novos dados ou envie lembretes
            except Exception as e:
                logger.exception("❌ Erro ao executar o ciclo")

        time.sleep(60 * 30)  # Espera 30 minutos

if __name__ == "__main__":
    loop_infinito()
