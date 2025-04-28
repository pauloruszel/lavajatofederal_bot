from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters
from handlers import start, agendar, receber_nome, receber_telefone, receber_tipo_lavagem, receber_data_horario, confirmar, listar_agendamentos
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

NOME, TELEFONE, TIPO_LAVAGEM, DATA_HORARIO, CONFIRMAR, ESCOLHER_CANCELAR = range(6)

def main():
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

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agendamentos", listar_agendamentos))
    app.add_handler(conv_handler)

    print("Bot do Lava Jato Federal iniciado...")
    app.run_polling()