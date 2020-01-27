from telegram.ext import ConversationHandler, MessageHandler, Filters

reply_text = 'Команда отменена 😌'

def cancel(update, context):
  update.message.reply_text(text=reply_text)
  return ConversationHandler.END

fallback = MessageHandler(Filters.regex('[/]'), cancel)