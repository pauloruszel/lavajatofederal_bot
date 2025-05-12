import os
import re
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from scheduler import agendar_lembrete
from utils import salvar_agendamento, listar_eventos_google_calendar
from helpers import normalizar_data_hora
from logger_config import setup_logging

logger = setup_logging()

NOME, TELEFONE, TIPO_LAVAGEM, DATA_HORARIO, CONFIRMAR, ESCOLHER_CANCELAR = range(6)
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"/start por usuário {user_id}")
    await update.message.reply_text(
        "Bem-vindo ao *Lava Jato Federal*!\n"
        "QS 11 Conjunto A Lote 121, Areal - Águas Claras/DF\n\n"
        "Serviços disponíveis:\n"
        "• Lavagem Simples - R$30\n"
        "• Lavagem Americana - R$40\n"
        "• Carro Grande - R$70\n"
        "• Polimento Técnico - a consultar\n\n"
        "Sistema Leva e Traz disponível!\n\n"
        "Para agendar, digite /agendar.",
        parse_mode='Markdown'
    )

async def agendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Início de agendamento por {update.effective_user.id}")
    context.user_data.clear()
    await update.message.reply_text("Ótimo! Vamos agendar sua lavagem.\nQual o seu nome completo?")
    return NOME

async def receber_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.message.text.strip()
    context.user_data['nome'] = nome
    logger.info(f"Nome informado: {nome}")
    await update.message.reply_text("Agora, informe seu telefone (com DDD):")
    return TELEFONE

async def receber_telefone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telefone = update.message.text.strip()
    context.user_data['telefone'] = telefone
    logger.info(f"Telefone informado: {telefone}")
    opcoes = [["Lavagem Simples"], ["Lavagem Americana"], ["Carro Grande"], ["Polimento Técnico"]]
    markup = ReplyKeyboardMarkup(opcoes, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Escolha o tipo de serviço:", reply_markup=markup)
    return TIPO_LAVAGEM

async def receber_tipo_lavagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tipo = update.message.text.strip()
    context.user_data['tipo_lavagem'] = tipo
    logger.info(f"Serviço escolhido: {tipo}")
    await update.message.reply_text("Informe a data e horário desejado (Ex: 27/04 às 14h ou 27/04 às 14h30):")
    return DATA_HORARIO

async def receber_data_horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data_horario = update.message.text.strip()
    texto = normalizar_data_hora(data_horario)

    try:
        datetime.strptime(texto, "%d/%m %H:%M")
    except Exception as e:
        logger.warning(f"Erro ao fazer parsing de data/hora: '{texto}' - {e}")
        await update.message.reply_text(
            "⚠️ *Formato inválido.* Tente algo como `12/05 às 14h` ou `12/05 às 14h30`.",
            parse_mode="Markdown"
        )
        return DATA_HORARIO

    context.user_data['data_horario'] = data_horario
    logger.info(f"Data/hora informado: {data_horario}")

    resumo = (
        f"*Resumo do seu agendamento:*\n\n"
        f"Nome: {context.user_data['nome']}\n"
        f"Telefone: {context.user_data['telefone']}\n"
        f"Serviço: {context.user_data['tipo_lavagem']}\n"
        f"Data e Horário: {context.user_data['data_horario']}\n\n"
        f"Digite *Confirmar* para finalizar ou *Cancelar* para abortar."
    )
    await update.message.reply_text(resumo, parse_mode='Markdown')
    return CONFIRMAR

async def confirmar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    texto = update.message.text.strip().lower()

    if texto == 'confirmar':
        try:
            salvar_agendamento(context.user_data)
            logger.info(f"✅ Agendamento salvo com sucesso para {user_id}: {context.user_data}")
        except ValueError as ve:
            logger.warning(f"⚠️ Conflito no agendamento para {user_id}: {ve}")
            await update.message.reply_text(
                f"⚠️ *Erro ao agendar:*\n{ve}\n\n"
                "Por favor, escolha outro horário e tente novamente com /agendar.",
                parse_mode='Markdown'
            )
            context.user_data.clear()
            return ConversationHandler.END
        except Exception as e:
            logger.error(f"❌ Erro inesperado ao salvar agendamento para {user_id}: {e}", exc_info=True)
            await update.message.reply_text("❌ Ocorreu um erro inesperado ao tentar agendar. Tente novamente mais tarde.")
            context.user_data.clear()
            return ConversationHandler.END

        try:
            await agendar_lembrete(update, context)
        except Exception as e:
            logger.error(f"❌ Falha ao agendar lembrete para {user_id}: {e}", exc_info=True)

        keyboard = [[InlineKeyboardButton("Falar no WhatsApp", url="https://wa.me/5561981944787")]]
        await update.message.reply_text(
            "✅ Agendamento confirmado! Muito obrigado.\nClique abaixo para falar conosco no WhatsApp:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        context.user_data.clear()
        return ConversationHandler.END

    else:
        logger.info(f"Agendamento cancelado por {user_id}")
        await update.message.reply_text("Agendamento cancelado. Se quiser agendar de novo, digite /agendar.")
        context.user_data.clear()
        return ConversationHandler.END

async def listar_agendamentos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id != ADMIN_ID:
        logger.warning(f"🔒 Acesso negado ao comando /agendamentos por {user_id}")
        await update.message.reply_text("Desculpe, este comando é restrito ao administrador.")
        return

    try:
        eventos = listar_eventos_google_calendar()
        if not eventos:
            logger.info("Nenhum agendamento encontrado.")
            await update.message.reply_text("Nenhum agendamento encontrado no Google Calendar.")
            return

        resposta = "*Agendamentos no Google Calendar:*\n\n"
        for idx, evento in enumerate(eventos, 1):
            inicio = evento['start'].get('dateTime', evento['start'].get('date'))
            resposta += f"{idx}. {evento.get('summary', 'Sem título')} | Início: {inicio}\n"

        logger.info("📋 Listagem de agendamentos realizada com sucesso.")
        await update.message.reply_text(resposta, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"❌ Erro ao listar agendamentos: {e}", exc_info=True)
        await update.message.reply_text("❌ Ocorreu um erro ao listar os agendamentos.")