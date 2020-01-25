from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

no_schedule = (
  'У меня нет твоего расписания.\n\n'
  'Не забудь задать свои данные, а затем вызвать /get_schedule, чтобы я сохранил твое расписание.'
)

action_call = (
  'Опаздываешь на лекции? Теперь не будешь 😝'
  'Введи количество минут от 1 до 120, и я буду оповещать тебя о лекциях, когда до них останется количество минут, которое ты указал.'
  'Введи 0, если хочешь, чтобы я перестал оповещать тебя о предстоящих лекциях.'
  'Введи /cancel, если вызвал команду по ошибке.'
)

STATE = 'NOTIFY_MINUTES'

def exit_conversation(update, context):
  print(456)
  chat_id = update.effective_chat.id
  context.bot.send_message(chat_id=chat_id, text="Exiting..")

def minutes_choice(update, context):
  print(123)
  chat_id = update.effective_chat.id
  try:
    minutes = int(update.message.text)
    text_to_send = None
    if minutes == 0:
        text_to_send = bot_messages.disable_notifying_minutes_response
    elif 0 < minutes and minutes < 120:
        text_to_send = bot_messages.successful_notifying_minutes_update_response
    else:
        text_to_send = bot_messages.no_notifying_minutes_response
    context.bot.send_message(chat_id=chat_id, text=text_to_send)
    if minutes < 0 or 120 < minutes:
        return ConversationHandler.END
    api_calls.update_schedule_notify_minutes(chat_id, minutes)
  except ValueError:
    send_message(bot, chat_id=chat_id, text=bot_messages.notifying_minutes_not_number_response)
  return ConversationHandler.END

def notify_lectures(update, context):
  chat_id = update.effective_chat.id
  context.bot.send_chatting_action(chat_id=chat_id, action=ChatAction.TYPING)

  chat_info = db.get_chat(chat_id)

  if not 'schedule' in chat_info:
    context.bot.send_message(chat_id=chat_id, text=no_schedule)
    return ConversationHandler.END

  context.bot.send_message(chat_id=chat_id, text=action_call)

  return STATE

# notify_lectures_handler = ConversationHandler(
#   entry_points=[CommandHandler('notify_lectures', notify_lectures)],
#   states={
#     STATE: [MessageHandler(Filters.text, minutes_choice)],
#   },
#   fallbacks=[CallbackQueryHandler(exit_conversation, pattern='Back')]
# )

def kek(update, context):
  print("Entering kek..")

  keyboard = [[InlineKeyboardButton("Option 1", callback_data='Back')]]
  reply_markup = InlineKeyboardMarkup(keyboard)
  update.message.reply_text('Please choose:', reply_markup=reply_markup)

  chat_id = update.effective_chat.id
  context.bot.send_message(chat_id=chat_id, text="Kekocity")
  return STATE

notify_lectures_handler = ConversationHandler(
  entry_points=[CommandHandler('notify_lectures', kek)],
  states={
    STATE: [MessageHandler(Filters.text, minutes_choice)],
  },
  fallbacks=[CallbackQueryHandler(exit_conversation, pattern='Back')]
)