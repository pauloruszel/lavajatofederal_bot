# 🚗 Bot Telegram - Lava Jato Federal

Um bot desenvolvido para facilitar o agendamento de lavagens de carros no Lava Jato Federal!  
Agende, consulte e receba lembretes automáticos diretamente pelo Telegram.

---

## 📋 Funcionalidades

- /start → Mensagem de boas-vindas com informações dos serviços.
- /agendar → Processo guiado de agendamento de lavagem:
  - Nome completo
  - Telefone
  - Tipo de lavagem (simples, americana, carro grande ou polimento técnico)
  - Data e horário desejado
- /agendamentos → (restrito ao administrador) Listagem de todos os agendamentos.
- Agendamento de lembrete automático 1 dia antes do serviço.
- Envio de botão para WhatsApp após confirmar o agendamento.

---

## 📂 Estrutura do Projeto

```plaintext
.
├── .env
├── agendamentos_lavajato.csv
├── bot_lavajato.py         # Arquivo de entrada (executar esse)
├── handlers.py             # Funções de fluxo de conversa e comandos
├── main.py                 # Monta os handlers e inicia o bot
├── requirements.txt        # Dependências
├── scheduler.py            # Controle de agendamento de lembretes
└── utils.py                # Funções utilitárias (validadores, helpers)
