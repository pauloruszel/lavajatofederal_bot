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
├── .env                     # Variáveis de ambiente (BOT_TOKEN, CALENDAR_ID, etc.)
├── .gitignore              # Arquivos e pastas ignorados pelo Git
├── bot_lavajato.py         # Arquivo principal para iniciar o bot
├── credentials.json        # Credenciais da conta de serviço do Google
├── handlers.py             # Fluxo de conversa e comandos do bot
├── helpers.py              # Funções auxiliares de normalização de data/hora
├── logger_config.py        # Configuração de logging do projeto
├── main.py                 # Registra e inicia os handlers do Telegram
├── README.md               # Documentação do projeto
├── requirements.txt        # Lista de dependências do projeto
├── scheduler.py            # Agendador de lembretes automáticos com APScheduler
└── utils.py                # Integração com Google Calendar e validações
```

---

## ⚙️ Requisitos

- Python 3.12
- Conta de serviço com acesso ao Google Calendar
- Bot Token do Telegram (gerado com o [@BotFather](https://t.me/BotFather))

---

## ▶️ Como Executar

1. **Clone o repositório:**

```bash
git clone https://github.com/seuusuario/lavajatofederal_bot.git
cd lavajatofederal_bot
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Configure o arquivo `.env` com as variáveis:**

```env
BOT_TOKEN=seu_token_telegram
CALENDAR_ID=seu_id_da_agenda_google@group.calendar.google.com
ADMIN_ID=123456789  # seu user_id do Telegram
```

4. **Adicione as credenciais do Google Calendar:**

- Crie um projeto e uma conta de serviço no [Google Cloud Console](https://console.cloud.google.com/)
- Habilite a API do Google Calendar
- Gere um arquivo JSON com as credenciais da conta de serviço e salve como `credentials.json`
- Compartilhe sua agenda com o e-mail da conta de serviço com permissão para **fazer alterações nos eventos**

5. **Execute o bot:**

```bash
python bot_lavajato.py
```

---

## 📌 Observações

- O bot reconhece datas no formato:  
  `12/05 às 15h`, `12/05 15h`, `12/05 às 15h30` etc.
- O horário é convertido para o fuso horário `America/Sao_Paulo`
- O lembrete é enviado 1 dia antes do agendamento (ou 1 minuto depois se estiver muito próximo)
- Após agendar, o usuário recebe botão para contato via WhatsApp

---

## 📞 Contato e Suporte

Em caso de dúvidas ou sugestões, entre em contato via WhatsApp após o agendamento ou crie uma [issue no GitHub](https://github.com/seuusuario/lavajatofederal_bot/issues)

---

## 👨‍💻 Autor

Desenvolvido com 💻 e ☕ por **Paulo Ruszel**  
📧 [paulo.ruszel.santos@gmail.com](mailto:paulo.ruszel.santos@gmail.com)