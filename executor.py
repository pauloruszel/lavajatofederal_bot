import os
import sys
import time
import signal
import atexit
from datetime import datetime
from bot_lavajato import main
from logger_config import setup_logging

logger = setup_logging()

PID_FILE = "/tmp/lavajatobot.pid"

def checar_instancia_unica():
    if os.path.exists(PID_FILE):
        logger.warning("🚫 Outra instância já está rodando. Abortando.")
        sys.exit()
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    logger.info(f"📌 PID registrado em {PID_FILE}")

def remover_pid():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
        logger.info("🧹 PID removido com sucesso.")

def sinal_encerramento(signum, frame):
    logger.warning(f"⚠️ Encerrando (signal {signum}). Limpando PID e saindo...")
    remover_pid()
    sys.exit(0)

# Configurações iniciais
checar_instancia_unica()
atexit.register(remover_pid)

# Captura sinais como CTRL+C ou finalização forçada
signal.signal(signal.SIGINT, sinal_encerramento)   # Ctrl+C
signal.signal(signal.SIGTERM, sinal_encerramento)  # kill PID ou interrupção do PythonAnywhere

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
