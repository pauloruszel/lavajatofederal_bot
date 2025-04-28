from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from scheduler import agendar_lembrete
from utils import salvar_agendamento, carregar_agendamentos
import os

NOME, TELEFONE, TIPO_LAVAGEM, DATA_HORARIO, CONFIRMAR, ESCOLHER_CANCELAR = range(6)
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    context.user_data.clear()
    await update.message.reply_text("Ótimo! Vamos agendar sua lavagem.\nQual o seu nome completo?")
    return NOME

async def receber_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nome'] = update.message.text.strip()
    await update.message.reply_text("Agora, informe seu telefone (com DDD):")
    return TELEFONE

async def receber_telefone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['telefone'] = update.message.text.strip()
    opcoes = [["Lavagem Simples"], ["Lavagem Americana"], ["Carro Grande"], ["Polimento Técnico"]]
    markup = ReplyKeyboardMarkup(opcoes, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Escolha o tipo de serviço:", reply_markup=markup)
    return TIPO_LAVAGEM

async def receber_tipo_lavagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['tipo_lavagem'] = update.message.text.strip()
    await update.message.reply_text("Informe a data e horário desejado (Ex: 27/04 às 14h ou 27/04 às 14h30):")
    return DATA_HORARIO

async def receber_data_horario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['data_horario'] = update.message.text.strip()
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
    texto = update.message.text.strip().lower()
    if texto == 'confirmar':
        salvar_agendamento(context.user_data)
        await agendar_lembrete(update, context)
        keyboard = [[InlineKeyboardButton("Falar no WhatsApp", url="https://wa.me/5561981944787")]]
        await update.message.reply_text(
            "Agendamento confirmado! Muito obrigado.\nClique abaixo para falar conosco no WhatsApp:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        context.user_data.clear()
        return ConversationHandler.END
    else:
        await update.message.reply_text("Agendamento cancelado. Se quiser agendar de novo, digite /agendar.")
        context.user_data.clear()
        return ConversationHandler.END

async def listar_agendamentos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        await update.message.reply_text("Desculpe, este comando é restrito ao administrador.")
        return
    agendamentos = carregar_agendamentos()
    if not agendamentos:
        await update.message.reply_text("Nenhum agendamento encontrado ainda.")
        return
    resposta = "*Lista de Agendamentos:*\n\n"
    for idx, a in enumerate(agendamentos, 1):
        resposta += f"{idx}. {a['nome']} | {a['telefone']} | {a['tipo_lavagem']} | {a['data_horario']}\n"
    await update.message.reply_text(resposta, parse_mode='Markdown')