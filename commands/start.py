from telegram.ext import CommandHandler 

response_text =  (
  'Привет 👋🏼, меня зовут Indigo!\n\n'
  'Я буду оповещать тебя о новых оценках, вебворках и буду подсказывать тебе расписание 😋\n\n'
  'Пропиши /help, чтобы увидеть список доступных команд.\n\n'
  'Удачи и высокого GPA!\n\n'
)

def handler(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

start_handler = CommandHandler('start', handler)