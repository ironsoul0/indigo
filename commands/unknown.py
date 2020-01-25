from telegram.ext import MessageHandler, Filters 

response_text = (
  "Прости, но я не знаю эту команду.\n\n"
  "Введи /help, чтобы увидеть список доступных команд."
)

def handler(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

unknown_handler = MessageHandler(Filters.command, handler)