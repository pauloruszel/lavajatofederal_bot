import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)
from handlers import (
    start,
    agendar,
    receber_nome,
    receber_telefone,
    receber_tipo_lavagem,
    receber_data_horario,
    confirmar,
    listar_agendamentos
)
from logger_config import setup_logging
logger = setup_logging()  # <- logger unificado

# Carrega variáveis de ambiente do .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Estados da conversa
NOME, TELEFONE, TIPO_LAVAGEM, DATA_HORARIO, CONFIRMAR, ESCOLHER_CANCELAR = range(6)

def main():
    if not TOKEN:
        logger.error("❌ TOKEN não definido. Verifique seu arquivo .env.")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('agendar', agendar)],
        states={
            NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_nome)],
            TELEFONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_telefone)],
            TIPO_LAVAGEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_tipo_lavagem)],
            DATA_HORARIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_data_horario)],
            CONFIRMAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmar)],
        },
        fallbacks=[CommandHandler('agendar', agendar)],
    )

    # Adiciona comandos ao bot
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agendamentos", listar_agendamentos))
    app.add_handler(conv_handler)

    logger.info("🚀 Bot do Lava Jato Federal iniciado com sucesso.")

    try:
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.exception("Erro ao rodar o bot:")