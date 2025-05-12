import os
import pytz
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil import parser
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from helpers import normalizar_data_hora
from logger_config import setup_logging

logger = setup_logging()

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'
CALENDAR_ID = os.getenv("CALENDAR_ID", "").strip()

if not CALENDAR_ID:
    raise ValueError("CALENDAR_ID não foi definido corretamente no .env")

def get_calendar_service():
    try:
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        return build('calendar', 'v3', credentials=creds)
    except Exception:
        logger.exception("❌ Erro ao criar serviço do Google Calendar.")
        raise

def verificar_conflito(service, inicio_iso, fim_iso):
    try:
        eventos = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=inicio_iso,
            timeMax=fim_iso,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        conflito = len(eventos.get('items', [])) > 0
        if conflito:
            logger.warning(f"⚠️ Conflito encontrado entre {inicio_iso} e {fim_iso}")
        return conflito

    except HttpError as e:
        logger.error(f"❌ Erro de API ao verificar conflito: {e}")
        raise

    except Exception:
        logger.exception("❌ Erro inesperado ao verificar conflito.")
        raise

def listar_eventos_google_calendar():
    try:
        service = get_calendar_service()
        agora = datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()

        eventos_resultado = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=agora,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        logger.info("📋 Eventos listados com sucesso.")
        return eventos_resultado.get('items', [])

    except Exception:
        logger.exception("❌ Erro ao listar eventos do Google Calendar.")
        return []

def salvar_agendamento(dados):
    try:
        raw = dados['data_horario']
        txt = normalizar_data_hora(raw)

        # Tenta fazer o parsing seguro
        momento = None
        for fmt in ("%d/%m %H:%M", "%d/%m %H"):
            try:
                momento = datetime.strptime(txt, fmt)
                break
            except ValueError:
                continue

        if momento is None:
            raise ValueError(f"Formato de data/hora inválido: {raw}")

        momento = momento.replace(year=datetime.now().year)

        tz = pytz.timezone('America/Sao_Paulo')
        momento = tz.localize(momento)

        inicio = momento.isoformat()
        fim = (momento + timedelta(hours=1)).isoformat()

        service = get_calendar_service()

        if verificar_conflito(service, inicio, fim):
            raise ValueError(f"Já existe um agendamento entre {inicio} e {fim}.")

        event = {
            'summary': f"Lavagem: {dados['tipo_lavagem']}",
            'description': f"Cliente: {dados['nome']}\nTelefone: {dados['telefone']}",
            'start': {'dateTime': inicio, 'timeZone': 'America/Sao_Paulo'},
            'end': {'dateTime': fim, 'timeZone': 'America/Sao_Paulo'},
        }

        criado = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        logger.info(f"✅ Evento criado com sucesso: {criado.get('htmlLink')}")

    except ValueError as ve:
        logger.warning(f"⚠️ Conflito ao salvar agendamento: {ve}")
        raise

    except Exception:
        logger.exception("❌ Erro inesperado ao salvar agendamento.")
        raise