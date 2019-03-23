from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, ConversationHandler, RegexHandler
from telegram import ForceReply
from telegram.error import BadRequest
from bs4 import BeautifulSoup
import requests
import os
import threading
import time

try:
  import sensitive
except ImportError:
  print(os.environ['BOT_TOKEN'])

import webwork_login
import api_calls
import bot_messages
import registrar_login
import time_helpers
import bot_states
import moodle_login
import mynuedu

def send_message(bot, chat_id, text):
  try:
    bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
  except:
    print('No such chat_id using a bot')

def send_sticker(bot, chat_id, sticker_id):
  try:
    bot.send_sticker(chat_id=chat_id, sticker=sticker_id)
  except:
    print('No such chat_id using a bot')

def unknown_command(bot, update):
  send_message(bot, 
    chat_id=update.message.chat_id, 
    text=bot_messages.unknown_command_response
  )

def start(bot, update):
  send_message(bot, 
    chat_id=update.message.chat_id, 
    text=bot_messages.start_command_response
  )

def username_choice(bot, update):
  new_username = update.message.text.lower()
  print('{} wants to join Indigo community'.format(new_username))
  update.message.reply_text(bot_messages.updated_login_response)  
  api_calls.update_username(update.message.chat_id, new_username)
  return ConversationHandler.END

def set_username(bot, update):
  update.message.reply_text(bot_messages.set_username_response, parse_mode='HTML')
  return bot_states.USERNAME_CHOICE 

def notify_about_new_webwork(bot, chat_id, course_name, new_webwork):
  send_message(bot, 
    chat_id=chat_id,
    text='{}{} - {}'.format(bot_messages.new_webwork_response, course_name, new_webwork)
  )

def check_new_webworks(bot, chat_id):
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
  
def webwork_password_choice(bot, update):
  new_password = update.message.text
  update.message.reply_text(bot_messages.updated_password_response)  
  api_calls.update_webwork_password(update.message.chat_id, new_password)
  return ConversationHandler.END

def set_webwork_password(bot, update):
  update.message.reply_text(bot_messages.set_webwork_password_response, parse_mode='HTML')
  return bot_states.WEBWORK_PASSWORD_CHOICE

def main_password_choice(bot, update):
  new_password = update.message.text
  update.message.reply_text(bot_messages.updated_password_response)  
  api_calls.update_main_password(update.message.chat_id, new_password)
  return ConversationHandler.END

def set_main_password(bot, update):
  update.message.reply_text(bot_messages.set_main_password_response, parse_mode='HTML')
  return bot_states.MAIN_PASSWORD_CHOICE

def help(bot, update):
  update.message.reply_text(bot_messages.help_command_response)  

def set_webworks_for_chat(chat_id, webworks):
  api_calls.update_webworks_for_chat(chat_id, webworks)

def notify_webwork(bot, update):
  chat_info = api_calls.get_chat_info(update.message.chat_id)
  if not 'webwork_password' in chat_info or not 'username' in chat_info:
    update.message.reply_text(bot_messages.no_login_or_password_response)
  else:
    send_message(bot, chat_id=update.message.chat_id, 
      text=bot_messages.checking_data_response)
    current_webworks = webwork_login.get_webworks(chat_info['username'], chat_info['webwork_password'])
    if 'fail' in current_webworks:
      send_message(bot, chat_id=update.message.chat_id, 
        text=bot_messages.wrong_webwork_data_response)
    else:
      send_message(bot, chat_id=update.message.chat_id, text=bot_messages.successful_webwork_login_response)
      for section, webworks in current_webworks.items():
        for webwork in webworks:
          send_message(bot, chat_id=update.message.chat_id, text='• {} - {}'.format(section, webwork))
      set_webworks_for_chat(update.message.chat_id, current_webworks)      
  
def notify_grades(bot, update):
  chat_info = api_calls.get_chat_info(update.message.chat_id)
  if not 'main_password' in chat_info or not 'username' in chat_info:
    update.message.reply_text(bot_messages.no_login_or_password_response)
  else:
    send_message(bot, chat_id=update.message.chat_id, 
      text=bot_messages.checking_data_response)
    current_grades = moodle_login.get_grades(chat_info['username'], chat_info['main_password'])
    if len(current_grades.keys()) == 0:
      send_message(bot, chat_id=update.message.chat_id, 
        text=bot_messages.wrong_registrar_data_response)
    else:
      send_message(bot, chat_id=update.message.chat_id, text=bot_messages.successful_moodle_login_response)
      set_grades_for_chat(update.message.chat_id, current_grades)
      
def set_grades_for_chat(chat_id, new_grades):
  api_calls.update_grades_for_chat(chat_id, new_grades)

def get_schedule(bot, update):
  chat_info = api_calls.get_chat_info(update.message.chat_id)
  if not 'main_password' in chat_info or not 'username' in chat_info:
    update.message.reply_text(bot_messages.no_login_or_password_response)
  else:
    send_message(bot, chat_id=update.message.chat_id, 
      text=bot_messages.checking_data_response)
    try:
      schedule = registrar_login.get_schedule(chat_info['username'], chat_info['main_password'])
      print('{} used /get_schedule command'.format(chat_info['username']))
      if len(schedule.keys()) == 0:
        send_message(bot, chat_id=update.message.chat_id, 
          text=bot_messages.wrong_registrar_data_response)
      else:
        send_message(bot, chat_id=update.message.chat_id, text=bot_messages.successful_registrar_login_response)
        api_calls.update_schedule_for_chat(update.message.chat_id, schedule)
    except:
      print('Schedule error....')

def show_schedule(bot, update):
  update.message.reply_text(bot_messages.wait_please_response)
  chat_id = update.message.chat_id
  chat_info = api_calls.get_chat_info(chat_id)
  if not 'schedule' in chat_info:
    send_message(bot, chat_id=chat_id, 
      text=bot_messages.no_schedule_response)
  else:
    print('{} used /show_schedule command'.format(chat_info['username']))
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
    send_message(bot, chat_id=chat_id, text=message)
      
def next_lecture(bot, update):
  chat_id = update.message.chat_id
  chat_info = api_calls.get_chat_info(chat_id)
  if not 'schedule' in chat_info:
    send_message(bot, chat_id=chat_id, 
      text=bot_messages.no_schedule_response)
  else:
    print('{} used /next_lecture command'.format(chat_info['username']))
    schedule = chat_info['schedule']
    current_day = time_helpers.current_day()
    current_time = time_helpers.current_time_in_minutes()
    if not current_day in schedule:
      schedule[current_day] = []
    for subject in schedule[current_day]:
      start_time = time_helpers.am_to_pm(subject['start_time'])
      if start_time > current_time:
        message = '<b>{}</b>\n\n'.format(current_day)
        message = message + '{}\n{} - {}\n{}\n'.format(
          subject['course_name'], 
          subject['start_time'], 
          subject['end_time'], 
          subject['lecture_room']
        ) 
        send_message(bot, chat_id=chat_id, text=message)
        return 
    days = time_helpers.days
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
        send_message(bot, chat_id=chat_id, text=message)
        return

def notify_minutes_choice(bot, update):
  chat_id = update.message.chat_id
  try:
    minutes = int(update.message.text)
    if not (minutes >= 0 and minutes <= 120):
      send_message(bot, chat_id=chat_id, text=bot_messages.no_notifying_minutes_response)
      return ConversationHandler.END
    if minutes > 0:
      send_message(bot, chat_id=chat_id, text=bot_messages.successful_notifying_minutes_update_response)
    else:
      send_message(bot, chat_id=chat_id, text=bot_messages.disable_notifying_minutes_response)
    api_calls.update_schedule_notify_minutes(chat_id, minutes)
  except ValueError:
    send_message(bot, chat_id=chat_id, text=bot_messages.notifying_minutes_not_number_response)

  return ConversationHandler.END

def notify_lectures(bot, update):
  chat_id = update.message.chat_id
  chat_info = api_calls.get_chat_info(chat_id)
  if not 'schedule' in chat_info:
    send_message(bot, chat_id=chat_id, text=bot_messages.no_schedule_response)
    return ConversationHandler.END
  update.message.reply_text(bot_messages.notify_lectures_response, parse_mode='HTML')
  return bot_states.NOTIFY_MINUTES_CHOICE

def notifying_webworks_process(bot):
  while True:
    if time_helpers.current_time_in_minutes() >= 0 and time_helpers.current_time_in_minutes() <= 719:
      continue
    print('Starting to notify about new webworks..')
    chats = api_calls.get_all_chats_info()
    for chat in chats:
      if chat['notify_webworks']:
        try:
          chat_id = chat['chat_id']
          check_new_webworks(bot, chat_id)
        except:
          print('Webworks exception occured but still running..')
          pass
    time.sleep(14400)

def notifying_lectures_process(bot):
  print('Starting to notify about upcoming lectures..')
  while True:
    if time_helpers.current_time_in_minutes() >= 60 and time_helpers.current_time_in_minutes() <= 480:
      continue
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
          if notify_minutes % 100 > 10 and notify_minutes % 100 < 20:
            right_word = 'минут'
          message = 'Урок ровно через <b>{} {}</b>, не опоздай 😉\n\n'.format(notify_minutes, right_word)
          message = message + '{}\n{} - {}\n{}\n'.format(
            subject['course_name'], 
            subject['start_time'], 
            subject['end_time'], 
            subject['lecture_room']
          ) 
          send_message(bot, chat_id=chat_id, text=message)
    time.sleep(60)

def notifying_grades_process(bot):
  rep = 0
  while True:
    if time_helpers.current_time_in_minutes() >= 60 and time_helpers.current_time_in_minutes() <= 480:
      continue
    rep += 1
    print('Starting to check for new grades.. {}'.format(rep))
    chats = api_calls.get_all_chats_info()
    total_number = len(chats)
    current_number = 0
    for chat in chats:
      current_number += 1
      if not 'notify_grades' in chat or not chat['notify_grades']:
        continue
      try:
        chat_id = chat['chat_id']
        username = chat['username']
        main_password = chat['main_password']
        print('Checking {} grades.. {}/{}'.format(username, current_number, total_number))
        current_grades = moodle_login.get_grades(username, main_password)
        if len(current_grades.keys()) == 0:
          send_message(bot, chat_id=chat_id, text=bot_messages.password_changed_response)
          api_calls.disable_notify_grades_for_chat(chat_id)
          continue
        old_grades = chat['grades']
        for course_name, course_grades in current_grades.items():
          if not course_name in old_grades:
            old_grades[course_name] = []
          for course_grade in course_grades:
            name = course_grade['name']
            grade = course_grade['grade']
            unique_grade = True
            for old_grade in old_grades[course_name]:
              old_name = old_grade['name']
              old_grade = old_grade['grade']
              if old_name == name and old_grade == grade:
                unique_grade = False
            if unique_grade and course_name.lower() != 'error' and name.lower() != 'error' and grade.lower() != 'error':
              send_message(bot, chat_id=chat_id, text='Бро, у тебя новая оценка!\n\n')
              info = '{} - <b>{}</b>\n'.format('Course name', course_name)
              info += '{} - <b>{}</b>\n'.format('Grade name', name)
              info += '{} - <b>{}</b>\n'.format('Grade', grade)
              if 'range' in course_grade and course_grade['range'].lower() != 'error':
                info += '{} - <b>{}</b>\n'.format('Range', course_grade['range'])
              if 'percentage' in course_grade and course_grade['percentage'].lower() != 'error':
                info += '{} - <b>{}</b>\n'.format('Percentage', course_grade['percentage'])    
              send_message(bot, chat_id=chat_id, text=info)
              if 'percentage' in course_grade and course_grade['percentage'].lower() != 'error':
                check_excellence(bot, chat_id, course_grade['percentage'])
              print('{} got a new grade'.format(username))
              print('{} - {} - {}'.format(course_name, name, grade))
        set_grades_for_chat(chat_id, current_grades)
      except:
        print('Grades exception occured but still running..')
        pass
    
def check_excellence(bot, chat_id, percentage):
  valid_percent = percentage[:-2]
  try:
    int_percent = int(float(valid_percent))
    if int_percent == 100:
      send_message(bot, chat_id, bot_messages.full_grade)
      send_sticker(bot, chat_id, 'CAADBQADWQMAAukKyAMKKaSA3iagGgI')
    elif int_percent > 90:
      send_message(bot, chat_id, bot_messages.almost_full_grade)
      send_sticker(bot, chat_id, 'CAADBQAEAwAC6QrIA4GkHRvuSRcMAg')
  except ValueError:
    pass

def feedback(bot, update):
  send_message(bot, chat_id=update.message.chat_id, text=bot_messages.feedback_command_response)

def done(bot, update):
  send_message(bot, chat_id=update.message.chat_id, text=bot_messages.command_cancel_response)
  return ConversationHandler.END

def notify_users(bot):
  chats = api_calls.get_all_chats_info()
  for chat in chats:
    chat_id = chat['chat_id']
    try:
      bot.send_sticker(chat_id=chat_id, sticker='CAADBQADWQMAAukKyAMKKaSA3iagGgI')
    except:
      pass
    #send_message(bot, chat_id=chat_id, text='Дорогие девушки, поздравляем вас с этим замечательным днем! Будьте счастливы и оставайтесь всегда такими же красивыми 😍')

def log_text(bot, update):
  chat_id = update.message.chat_id
  chat_info = api_calls.get_chat_info(chat_id)
  if 'username' in chat_info:
    print('{} wrote {} to Indigo'.format(chat_info['username'], update.message.text))  

def main():
  updater = None

  if 'BOT_TOKEN' in os.environ:
    updater = Updater(os.environ['BOT_TOKEN'])
  else:
    updater = Updater(sensitive.secret_token)

  #notify_users(updater.bot)
  #check_excellence(updater.bot, sensitive.PERSON_ID, '100.00 %')

  notifying_lectures = threading.Thread(target=notifying_lectures_process, args=(updater.bot, ))
  notifying_webworks = threading.Thread(target=notifying_webworks_process, args=(updater.bot, ))
  notifying_grades = threading.Thread(target=notifying_grades_process, args=(updater.bot, ))
  threads = [notifying_lectures, notifying_webworks, notifying_grades]
  threads = [notifying_webworks, notifying_grades]
  threads = []

  for thread in threads:
    thread.start()

  start_handler = CommandHandler('start', start)
  help_handler = CommandHandler('help', help)
  get_schedule_handler = CommandHandler('get_schedule', get_schedule)
  show_schedule_handler = CommandHandler('show_schedule', show_schedule)
  notify_webwork_handler = CommandHandler('notify_webwork', notify_webwork)
  notify_grades_handler = CommandHandler('notify_grades', notify_grades)
  next_lecture_handler = CommandHandler('next_lecture', next_lecture)
  feedback_handler = CommandHandler('feedback', feedback)
  any_message_handler = MessageHandler(Filters.text, log_text)
  unknown_command_handler = MessageHandler(Filters.command, unknown_command)
  
  set_username_handler = ConversationHandler(
    entry_points=[CommandHandler('set_username', set_username)],
    states={
      bot_states.USERNAME_CHOICE: [MessageHandler(Filters.text, username_choice)]
    },
    fallbacks=[RegexHandler('[/]*', done)]
  )

  set_main_password_handler = ConversationHandler(
    entry_points=[CommandHandler('set_main_password', set_main_password)],
    states={
      bot_states.MAIN_PASSWORD_CHOICE: [MessageHandler(Filters.text, main_password_choice)]
    },
    fallbacks=[RegexHandler('[/]*', done)]
  )

  set_webwork_password_handler = ConversationHandler(
    entry_points=[CommandHandler('set_webwork_password', set_webwork_password)],
    states={
      bot_states.WEBWORK_PASSWORD_CHOICE: [MessageHandler(Filters.text, webwork_password_choice)]
    },
    fallbacks=[RegexHandler('[/]*', done)]
  )

  notify_lectures_handler = ConversationHandler(
    entry_points=[CommandHandler('notify_lectures', notify_lectures)],
    states={
      bot_states.NOTIFY_MINUTES_CHOICE: [MessageHandler(Filters.text, notify_minutes_choice)]
    },
    fallbacks=[RegexHandler('[/]*', done)]
  )

  updater.dispatcher.add_handler(set_username_handler)
  updater.dispatcher.add_handler(start_handler)
  updater.dispatcher.add_handler(set_webwork_password_handler)
  updater.dispatcher.add_handler(set_main_password_handler)
  updater.dispatcher.add_handler(show_schedule_handler)
  updater.dispatcher.add_handler(help_handler)
  updater.dispatcher.add_handler(notify_webwork_handler)
  updater.dispatcher.add_handler(get_schedule_handler)
  updater.dispatcher.add_handler(next_lecture_handler)
  updater.dispatcher.add_handler(notify_lectures_handler)
  updater.dispatcher.add_handler(notify_grades_handler)
  updater.dispatcher.add_handler(notify_grades_handler)
  updater.dispatcher.add_handler(feedback_handler)
  updater.dispatcher.add_handler(any_message_handler)
  updater.dispatcher.add_handler(unknown_command_handler)

  updater.start_polling()

if __name__ == '__main__':
  main()
