from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, ConversationHandler
from telegram import ForceReply
from bs4 import BeautifulSoup
import requests
import json

import webwork_login
import api_calls
import bot_messages
import bot_token
import registrar_login
import time_helpers
import bot_states

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
    text='{}{} - {}'.format(bot_messages.new_webwork_response, course_name, new_webwork)
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

def set_main_password(bot, update, args):
  if len(args) == 0:
    update.message.reply_text(bot_messages.empty_password_response)
  else:
    new_password = args[0]
    update.message.reply_text(bot_messages.updated_password_response)  
    api_calls.update_main_password(update.message.chat_id, new_password)

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
        text=bot_messages.wrong_webwork_data_response)
    else:
      bot.send_message(chat_id=update.message.chat_id, text=bot_messages.successful_webwork_login_response)
      for section, webworks in current_webworks.items():
        for webwork in webworks:
          bot.send_message(chat_id=update.message.chat_id, text='• {} - {}'.format(section, webwork))
      set_webworks_for_chat(update.message.chat_id, current_webworks)      
  
def get_schedule(bot, update):
  chat_info = api_calls.get_chat_info(update.message.chat_id)
  if not 'main_password' in chat_info or not 'username' in chat_info:
    update.message.reply_text(bot_messages.no_login_or_password_response)
  else:
    bot.send_message(chat_id=update.message.chat_id, 
      text=bot_messages.checking_data_response)
    schedule = registrar_login.get_schedule(chat_info['username'], chat_info['main_password'])
    print(schedule)
    if len(schedule.keys()) == 0:
      bot.send_message(chat_id=update.message.chat_id, 
        text=bot_messages.wrong_registrar_data_response)
    else:
      bot.send_message(chat_id=update.message.chat_id, text=bot_messages.successful_registrar_login_response)
      api_calls.update_schedule_for_chat(update.message.chat_id, schedule)

def show_schedule(bot, update):
  update.message.reply_text(bot_messages.wait_please_response)
  chat_id = update.message.chat_id
  chat_info = api_calls.get_chat_info(chat_id)
  if not 'schedule' in chat_info:
    bot.send_message(chat_id=chat_id, 
      text=bot_messages.no_schedule_response)
  else:
    schedule = chat_info['schedule']
    message = ''
    for day, subjects in schedule.items():
      message = message + '<b>{}</b>\n\n'.format(day)
      if len(subjects) == 0:
        message = message + bot_messages.no_lectures_this_day
      for subject in subjects:
        message = message + '{}\n{} - {}\n{}\n'.format(
          subject['course_name'], 
          subject['start_time'], 
          subject['end_time'], 
          subject['lecture_room']
        )
        message = message + '\n'
    bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
      
def next_lecture(bot, update):
  chat_id = update.message.chat_id
  chat_info = api_calls.get_chat_info(chat_id)
  if not 'schedule' in chat_info:
    bot.send_message(chat_id=chat_id, 
      text=bot_messages.no_schedule_response)
  else:
    schedule = chat_info['schedule']
    current_day = time_helpers.current_day()
    print(current_day)
    current_time = time_helpers.current_time_in_minutes()
    if not current_day in schedule:
      schedule[current_day] = []
    for subject in schedule[current_day]:
      start_time = time_helpers.am_to_pm(subject['start_time'])
      if start_time > current_time:
        message = '<b>{}</b>\n\n'.format(current_day, parse_mode='HTML')
        message = message + '{}\n{} - {}\n{}\n'.format(
          subject['course_name'], 
          subject['start_time'], 
          subject['end_time'], 
          subject['lecture_room']
        ) 
        bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
        return 
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_index = days.index(current_day)
    for index in range(0, len(days)):
      next_index = (day_index + index + 1) % 7
      next_day = days[next_index]
      if not next_day in schedule:
        continue
      for subject in schedule[next_day]:
        start_time = time_helpers.am_to_pm(subject['start_time'])
        message = '<b>{}</b>\n\n'.format(next_day)
        message = message + '{}\n{} - {}\n{}\n'.format(
          subject['course_name'], 
          subject['start_time'], 
          subject['end_time'], 
          subject['lecture_room']
        ) 
        bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
        return

def notify_lectures(bot, update, args):
  chat_id = update.message.chat_id
  if len(args) == 0:
    bot.send_message(chat_id=chat_id, text=bot_messages.no_notifying_minutes_response)
    return
  try:
    minutes = int(args[0])
    if not (minutes > 0 and minutes <= 120):
      bot.send_message(chat_id=chat_id, text=bot_messages.no_notifying_minutes_response)
      return
    chat_info = api_calls.get_chat_info(chat_id)
    if not 'schedule' in chat_info:
      bot.send_message(chat_id=chat_id, text=bot_messages.no_schedule_response)
      return
    bot.send_message(chat_id=chat_id, text=bot_messages.successful_notifying_minutes_update_response)
    api_calls.update_schedule_notify_minutes(chat_id, minutes)
  except ValueError:
    bot.send_message(chat_id=chat_id, text=bot_messages.notifying_minutes_not_number_response)

def notifying_webworks_process(bot, job):
  chats = api_calls.get_all_chats_info()
  for chat in chats:
    print(chat)
    if chat['notify_webworks']:
      chat_id = chat['chat_id']
      check_new_webworks(bot, chat_id)

def notifying_lectures_process(bot, job):
  chats = api_calls.get_all_chats_info()
  for chat in chats:
    notify_minutes = chat['schedule_notify_minutes']
    if notify_minutes == 0:
      continue
    chat_id = chat['chat_id']
    schedule = chat['schedule']
    current_day = time_helpers.current_day()
    current_minutes = time_helpers.current_time_in_minutes()
    if not current_day in schedule:
      continue 
    for subject in schedule[current_day]:
      subject_start_time = time_helpers.am_to_pm(subject['start_time'])
      if subject_start_time - current_minutes == notify_minutes:
        right_word = 'минут'
        if (notify_minutes % 10 == 1):
          right_word = 'минуту'
        elif (notify_minutes % 10 > 1 and notify_minutes % 10 < 5):
          right_word = 'минуты'
        message = 'Урок ровно через {} {}, не опоздай ;)\n\n'.format(notify_minutes, right_word)
        message = message + '{}\n{} - {}\n{}\n'.format(
          subject['course_name'], 
          subject['start_time'], 
          subject['end_time'], 
          subject['lecture_room']
        ) 
        bot.send_message(chat_id=chat_id, text=message)
        return


def main():
  updater = Updater(bot_token.secret_token)
  
  job = updater.job_queue
  job.run_repeating(notifying_webworks_process, interval=10, first=0)
  job.run_repeating(notifying_lectures_process, interval=60, first=0)
  
  start_handler = CommandHandler('start', start)
  help_handler = CommandHandler('help', help)
  get_schedule_handler = CommandHandler('get_schedule', get_schedule)
  show_schedule_handler = CommandHandler('show_schedule', show_schedule)
  set_username_handler = CommandHandler('set_username', set_username, pass_args=True)
  set_webwork_password_handler = CommandHandler('set_webwork_password', set_webwork_password, pass_args=True)
  set_main_password_handler = CommandHandler('set_main_password', set_main_password, pass_args=True)
  notify_webwork_handler = CommandHandler('notify_webwork', notify_webwork)
  next_lecture_handler = CommandHandler('next_lecture', next_lecture)
  notify_lectures_handler = CommandHandler('notify_lectures', notify_lectures, pass_args=True)
  unknown_command_handler = MessageHandler(Filters.command, unknown_command)
  
  updater.dispatcher.add_handler(start_handler)
  updater.dispatcher.add_handler(set_username_handler)
  updater.dispatcher.add_handler(set_webwork_password_handler)
  updater.dispatcher.add_handler(set_main_password_handler)
  updater.dispatcher.add_handler(show_schedule_handler)
  updater.dispatcher.add_handler(help_handler)
  updater.dispatcher.add_handler(notify_webwork_handler)
  updater.dispatcher.add_handler(get_schedule_handler)
  updater.dispatcher.add_handler(next_lecture_handler)
  updater.dispatcher.add_handler(notify_lectures_handler)
  updater.dispatcher.add_handler(unknown_command_handler)
  
  updater.start_polling()

if __name__ == '__main__':
  main()
