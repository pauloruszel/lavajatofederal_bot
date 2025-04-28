from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()
scheduler.start()

async def agendar_lembrete(update, context):
    chat_id = update.message.chat_id
    data_hora_str = context.user_data['data_horario'].replace("ás", "às").replace("as", "às").replace("As", "às").strip()
    try:
        try:
            data_hora = datetime.strptime(data_hora_str, "%d/%m às %Hh%M")
        except ValueError:
            data_hora = datetime.strptime(data_hora_str, "%d/%m às %Hh")
        data_hora = data_hora.replace(year=datetime.now().year)
        lembrete_hora = data_hora - timedelta(days=1)
        if lembrete_hora < datetime.now():
            lembrete_hora = datetime.now() + timedelta(minutes=1)
        scheduler.add_job(
            enviar_lembrete,
            trigger='date',
            run_date=lembrete_hora,
            args=[context.bot, chat_id, context.user_data.copy()]
        )
    except Exception as e:
        print(f"Erro ao agendar lembrete: {e}")

async def enviar_lembrete(bot, chat_id, user_data):
    try:
        horario = user_data['data_horario'].split('às ')[1] if 'às' in user_data['data_horario'] else user_data['data_horario']
        await bot.send_message(
            chat_id=chat_id,
            text=f"Olá {user_data['nome']}!\n"
                 f"Estamos lembrando que seu serviço de *{user_data['tipo_lavagem']}* "
                 f"está agendado para amanhã às {horario}.\n"
                 f"QS 11 Conjunto A Lote 121 - Areal, Águas Claras/DF\n\nLava Jato Federal!",
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Erro ao enviar lembrete: {e}")