from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from bs4 import BeautifulSoup
import requests
import json

import webwork_login
import api_calls
import bot_messages
import bot_token

def unknown_command(bot, update):
  bot.send_message(
    chat_id=update.message.chat_id, 
    text=bot_messages.unknown_command_response
  )

def start(bot, update):
  bot.send_message(
    chat_id=update.message.chat_id, 
    text=bot_messages.start_command_response
  )

def set_username(bot, update, args):
  if len(args) == 0:
    update.message.reply_text(bot_messages.empty_login_response)
  else:
    new_username = args[0]
    update.message.reply_text(bot_messages.updated_login_response)  
    api_calls.update_username(update.message.chat_id, new_username)
    
def notify_about_new_webwork(bot, chat_id, course_name, new_webwork):
  bot.send_message(
    chat_id=chat_id,
    text='{}{} - {}'.format(bot_messages.new_webwork_reponse, course_name, new_webwork)
  )

def check_new_webworks(bot, chat_id):
  #bot.send_message(chat_id=job.context, 
    #text='Checking new webworks..')
  
  chat_info = api_calls.get_chat_info(chat_id)
  username = chat_info['username']
  password = chat_info['webwork_password']
  old_webworks = chat_info['webworks']

  current_webworks = webwork_login.get_webworks(username, password)
  if 'fail' in current_webworks:
    return

  #current_webworks['T1mka'] = ['web1', 'web2']
  #current_webworks['almat'] = ['web1', 'web2']
  #current_webworks['webwork2/MATH-162-1L-Calc-II-Spring19'].append('web3')

  for course_name, webworks in current_webworks.items():
    for new_webwork in webworks:
      if (not course_name in old_webworks) or (not new_webwork in old_webworks[course_name]):
        notify_about_new_webwork(bot, chat_id, course_name, new_webwork)
  set_webworks_for_chat(chat_id, current_webworks)
  

def set_webwork_password(bot, update, args):
  if len(args) == 0:
    update.message.reply_text(bot_messages.empty_password_response)
  else:
    new_password = args[0]
    update.message.reply_text(bot_messages.updated_password_response)  
    api_calls.update_webwork_password(update.message.chat_id, new_password)

def help(bot, update):
  update.message.reply_text(bot_messages.help_command_response)  

def set_webworks_for_chat(chat_id, webworks):
  api_calls.update_webworks_for_chat(chat_id, webworks)
  print('Done!')

def notify_webwork(bot, update):
  chat_info = api_calls.get_chat_info(update.message.chat_id)
  print(chat_info)
  print('webwork_password' in chat_info)
  if not 'webwork_password' in chat_info or not 'username' in chat_info:
    update.message.reply_text(bot_messages.no_login_or_password_response)
  else:
    bot.send_message(chat_id=update.message.chat_id, 
      text=bot_messages.checking_data_response)
    current_webworks = webwork_login.get_webworks(chat_info['username'], chat_info['webwork_password'])
    if 'fail' in current_webworks:
      bot.send_message(chat_id=update.message.chat_id, 
        text=bot_messages.wrong_data_response)
    else:
      bot.send_message(chat_id=update.message.chat_id, text=bot_messages.successful_webwork_login_response)
      for section, webworks in current_webworks.items():
        for webwork in webworks:
          bot.send_message(chat_id=update.message.chat_id, text='• {} - {}'.format(section, webwork))
      set_webworks_for_chat(update.message.chat_id, current_webworks)      

def notifying_process(bot, job):
  chats = api_calls.get_all_chats_info()
  for chat in chats:
    print(chat)
    if chat['notify_webworks']:
      chat_id = chat['chat_id']
      check_new_webworks(bot, chat_id)

def main():
  updater = Updater(bot_token.secret_token)
  
  job = updater.job_queue
  job.run_repeating(notifying_process, interval=10, first=0)
  
  start_handler = CommandHandler('start', start)
  help_handler = CommandHandler('help', help)
  set_username_handler = CommandHandler('set_username', set_username, pass_args=True)
  set_webwork_password_handler = CommandHandler('set_webwork_password', set_webwork_password, pass_args=True)
  notify_webwork_handler = CommandHandler('notify_webwork', notify_webwork)
  unknown_command_handler = MessageHandler(Filters.command, unknown_command)
  
  updater.dispatcher.add_handler(start_handler)
  updater.dispatcher.add_handler(set_username_handler)
  updater.dispatcher.add_handler(set_webwork_password_handler)
  updater.dispatcher.add_handler(help_handler)
  updater.dispatcher.add_handler(notify_webwork_handler)
  updater.dispatcher.add_handler(unknown_command_handler)
  updater.start_polling()

if __name__ == '__main__':
  main()