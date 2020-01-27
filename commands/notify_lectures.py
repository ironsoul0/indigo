from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from enum import Enum

from helpers import end_conversation
import api_calls

class States(Enum):
  NOTIFY_MINUTES = 'NOTIFY_MINUTES'

def minutes_choice(update, context):
  chat_id = update.effective_chat.id
  try:
    minutes = int(update.message.text)
    text_to_send = None
    if minutes == 0:
      text_to_send = Messages.disable_feature
    elif 0 < minutes and minutes <= 120:
      text_to_send = Messages.success_result
    else:
      text_to_send = Messages.invalid_number
    context.bot.send_message(chat_id=chat_id, text=text_to_send)
    if minutes < 0 or 120 < minutes:
      return ConversationHandler.END
    api_calls.update_schedule_notify_minutes(chat_id, minutes)
  except ValueError:
    context.bot.send_message(chat_id=chat_id, text=Messages.invalid_number)
  return ConversationHandler.END

def notify_lectures(update, context):
  chat_id = update.effective_chat.id
  context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

  #TODO: Change to DB call
  chat_info = api_calls.get_chat_info(chat_id)

  if not 'schedule' in chat_info:
    context.bot.send_message(chat_id=chat_id, text=Messages.no_schedule)
    return ConversationHandler.END

  context.bot.send_message(chat_id=chat_id, text=Messages.action_call)

  return States.NOTIFY_MINUTES

notify_lectures_handler = ConversationHandler(
  entry_points=[CommandHandler('notify_lectures', notify_lectures)],
  states={
    States.NOTIFY_MINUTES: [MessageHandler(Filters.text, minutes_choice)],
  },
  fallbacks=[end_conversation.fallback] 
)

class Messages:
  no_schedule = (
    'У меня нет твоего расписания.\n\n'
    'Не забудь задать свои данные, а затем вызвать /get_schedule, чтобы я сохранил твое расписание.'
  )

  action_call = (
    'Опаздываешь на лекции? Теперь не будешь 😝\n\n'
    'Введи количество минут от 1 до 120, и я буду оповещать тебя о лекциях, когда до них останется количество минут, которое ты указал.\n\n'
    'Введи 0, если хочешь, чтобы я перестал оповещать тебя о предстоящих лекциях.\n\n'
    'Введи /cancel, если вызвал команду по ошибке.'
  )

  disable_feature = (
    'Больше не буду уведмолять тебя о предстоящих лекциях 🙂'
  )

  success_result = (
    'Кул! Теперь ты никогда не будешь опаздывать на уроки.'
  )

  invalid_number = (
    'Количество минут должно быть числом от 0 до 120!'
  )