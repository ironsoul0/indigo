from telegram.ext import MessageHandler, Filters 

def handler(update, context):
  update.message.reply_text(response_text)

unknown_handler = MessageHandler(Filters.command, handler)

response_text = (
  "Прости, но я не знаю эту команду.\n\n"
  "Введи /help, чтобы увидеть список доступных команд."
)
