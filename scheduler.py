from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from dateutil import parser
import pytz
import re
from logger_config import setup_logging

logger = setup_logging()

# Inicializa o agendador
scheduler = BackgroundScheduler()
scheduler.start()

async def agendar_lembrete(update, context):
    chat_id = update.message.chat_id
    data_hora_str = context.user_data['data_horario']

    try:
        # 🔧 Normaliza a string de data/hora com regex
        data_hora_str = (
            data_hora_str.replace("ás", "às")
                         .replace("as", "às")
                         .replace("As", "às")
                         .replace("às", "")
                         .replace("h", ":")
        )
        data_hora_str = re.sub(r"\s+", " ", data_hora_str).strip()
        data_hora_str = re.sub(r":\s*$", "", data_hora_str)

        data_hora = parser.parse(data_hora_str, dayfirst=True)
        data_hora = data_hora.replace(year=datetime.now().year)

        # Aplica timezone corretamente
        tz = pytz.timezone("America/Sao_Paulo")
        data_hora = tz.localize(data_hora)
        agora = datetime.now(tz)

        # Define horário do lembrete
        lembrete_hora = data_hora - timedelta(days=1)
        if lembrete_hora < agora:
            lembrete_hora = agora + timedelta(minutes=1)

        scheduler.add_job(
            enviar_lembrete,
            trigger='date',
            run_date=lembrete_hora,
            args=[context.bot, chat_id, context.user_data.copy()]
        )
        logger.info(f"⏰ Lembrete agendado para {lembrete_hora} (chat_id: {chat_id})")

    except Exception as e:
        logger.error("❌ Erro ao agendar lembrete", exc_info=True)

async def enviar_lembrete(bot, chat_id, user_data):
    try:
        horario = user_data['data_horario'].split('às')[-1].strip() if 'às' in user_data['data_horario'] else user_data['data_horario']

        await bot.send_message(
            chat_id=chat_id,
            text=f"Olá {user_data['nome']}!\n"
                 f"Estamos lembrando que seu serviço de *{user_data['tipo_lavagem']}* "
                 f"está agendado para amanhã às {horario}.\n"
                 f"QS 11 Conjunto A Lote 121 - Areal, Águas Claras/DF\n\nLava Jato Federal!",
            parse_mode='Markdown'
        )
        logger.info(f"📨 Lembrete enviado para {user_data['nome']} (chat_id: {chat_id})")

    except Exception as e:
        logger.error("❌ Erro ao enviar lembrete", exc_info=True)