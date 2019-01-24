from telegram.ext import CommandHandler
from telegram.ext import Updater
import requests
import json
import re
from bs4 import BeautifulSoup
import check

def tryToLogin(url, login, passwd):    
  result = [] 
  response = requests.post(url, files={'user': (None, login), 'passwd': (None, passwd)})
  successPat = re.compile(r'Logged in as {}'.format(login))    
  if successPat.search(response.text):
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.table.find_all('tr')
    for tr in trs:
      tds = tr.find_all('td')
      if len(tds) > 1:
        result.append('{} - {}'.format(tds[1].text, tds[2].text)) 
    return result
  else:
    raise("Couldn't login")

def loginToAll(login, passwd):
    print(login, passwd)
    url = "http://webwork.sst.nu.edu.kz/"
    pageText = requests.get(url).text
    loginLinkPat = re.compile(r'<a href="/(.+?)/">(.+?)</a>')
    link_list = []
    cnt = 0
    for match in loginLinkPat.finditer(pageText):
        link_list.append(match.group(1))    
    
    courses = {}

    for course in link_list: 
        try:
            sets = tryToLogin(url + course, login, passwd)
            courses[course] = sets
            cnt += 1
        except:
            pass
    if cnt == 0:
      return {'fail': [ ]}
    return courses


API_URL = 'https://nu-bot-backend.herokuapp.com/chat'

def callback_minute(bot, job):
  bot.send_message(chat_id=job.context, 
    text='One message every minute')

def callback_timer(bot, update, job_queue):
  bot.send_message(chat_id=update.message.chat_id, 
    text='Every 10 seconds - one message') 
  job_queue.run_repeating(callback_minute, interval=10, first=0, context=update.message.chat_id)

def start(bot, update):
  bot.send_message(chat_id=update.message.chat_id,
    text= "Привет, меня зовут Indigo!" \
          "\n" \
          "\n" \
          "Я буду оповещать тебя о новых вебворках и оценках :)" \
          "\n" \
          "Все данные, которые ты доверишь мне будут в безопасности, поэтому можешь ни чуть не переживать." \
          "\n" \
          "\n" \
          "Пропиши /help, чтобы увидеть список доступных команд." \
          "\n" \
          "\n" \
          "Удачи и высокого GPA!"
  )

def set_username(bot, update, args):
  if len(args) == 0:
    update.message.reply_text("Логин не должен быть пустым :)")
  else:
    payload = {
      'username': args[0],
    }
    headers = {
      'content-type': 'application/json; charset=utf-8'
    }
    update.message.reply_text("Прекрасно, я обновил твой логин!")  
    requests.post(
      '{}/set_username/{}'.format(API_URL, update.message.chat_id),
      data=json.dumps(payload),
      headers=headers
    )
    
def check_new_webworks(bot, chat_id):
  #bot.send_message(chat_id=job.context, 
    #text='Nurda dalbaeb..')
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  res = requests.get(
    '{}/{}'.format(API_URL, chat_id),
    headers=headers
  )
  res = json.loads(res.text)
  username = res['username']
  password = res['webwork_password']
  oldWebworks = res['webworks']
  currentWebworks = loginToAll(username, password)
  if 'fail' in currentWebworks:
    return
  print(type(oldWebworks))
  #currentWebworks['T1mka'] = ['web1', 'web2']
  #currentWebworks['almat'] = ['web1', 'web2']
  #currentWebworks['webwork2/MATH-162-1L-Calc-II-Spring19'].append('web3')


  for courseName, webworks in currentWebworks.items():
    for newWebwork in webworks:
      print(newWebwork)
      if not courseName in oldWebworks:
        bot.send_message(chat_id=chat_id,
          text='New webwork!\n{} - {}'.format(courseName, newWebwork)
        )
      elif not newWebwork in oldWebworks[courseName]:
        bot.send_message(chat_id=chat_id,
          text='New webwork!\n{} - {}'.format(courseName, newWebwork)
        )    

  print('currentWebworks')
  print(currentWebworks)

  payload = {
    'new_webworks': currentWebworks
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  res = requests.put(
    '{}/update_webworks/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )
  print('Worked?')


def set_webwork_password(bot, update, args):
  if len(args) == 0:
    update.message.reply_text("Пароль не должен быть пустым :)")
  else:
    payload = {
      'webwork_password': args[0],
    }
    headers = {
      'content-type': 'application/json; charset=utf-8'
    }
    update.message.reply_text("Отлично, я обновил твой пароль!")
    requests.post(
      '{}/set_webwork_password/{}'.format(API_URL, update.message.chat_id),
      data=json.dumps(payload),
      headers=headers
    )
    
def help(bot, update):
  update.message.reply_text(
    "Доступные команды:" \
    "\n" \
    "\n" \
    "1. /set_username <your_username> - твой username это строка вида name.surname" \
    "\n" \
    "2. /set_webwork_password <your_password> - обычно пароль от webwork'ов это твой Student ID" \
    "\n" \
    "3. /notify_webwork - если ты сообщил мне правильные данные, эта команда начнет оповещать тебя о новых webwork'ах в твоем аккаунте" \
    "\n" \
    "4. /help - показывает все доступные команды" \
  )  

def set_webworks_for_chat(chat_id, courses):
  payload = {
    'new_webworks': courses
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  requests.put(
    '{}/update_webworks/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )
  print('Done!')


def notify_webwork(bot, update, job_queue):
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  res = requests.get(
    '{}/{}'.format(API_URL, update.message.chat_id),
    headers=headers
  )
  res = json.loads(res.text)
  print(res)
  print('webwork_password' in res)
  if not 'webwork_password' in res or not 'username' in res:
    update.message.reply_text('Пожалуйста укажи свой логин и пароль. \n \nВведи /help, если понадобится помощь.')
  else:
    bot.send_message(chat_id=update.message.chat_id, 
    text='Один момент. Я проверю твои данные.')
    res = loginToAll(res['username'], res['webwork_password'])
    if 'fail' in res:
      bot.send_message(chat_id=update.message.chat_id, 
      text='Похоже ты ввел неправильные данные, или ты не зарегистрирован ни на один из курсов :(')
    else:
      bot.send_message(chat_id=update.message.chat_id, text='Отлично! Теперь я буду уведомлять тебя о новых вебворках.\nНа данный момент у тебя есть следующие вебворки:')
      for section, webworks in res.items():
        for webwork in webworks:
          bot.send_message(chat_id=update.message.chat_id, text='• {} - {}'.format(section, webwork))
      set_webworks_for_chat(update.message.chat_id, res)
      #print(job_check)
      

def notifying_process(bot, job):
  res = requests.get(
    '{}/all_chats'.format(API_URL)
  )
  res = json.loads(res.text)
  chats = res['chats']
  for chat in chats:
    print(chat)
    if chat['notify_webworks']:
      chat_id = chat['chat_id']
      check_new_webworks(bot, chat_id)

def main():
  u = Updater('703572266:AAEztdIDnTV6ka_3AZceqp1SjJDCDB3O2UU')
  j = u.job_queue
  j.run_repeating(notifying_process, interval=10, first=0)
  start_handler = CommandHandler('start', start)
  help_handler = CommandHandler('help', help)
  timer_handler = CommandHandler('timer', callback_timer, pass_job_queue=True)
  set_username_handler = CommandHandler('set_username', set_username, pass_args=True)
  set_webwork_password_handler = CommandHandler('set_webwork_password', set_webwork_password, pass_args=True)
  notify_webwork_handler = CommandHandler('notify_webwork', notify_webwork, pass_job_queue=True)
  u.dispatcher.add_handler(timer_handler)
  u.dispatcher.add_handler(start_handler)
  u.dispatcher.add_handler(set_username_handler)
  u.dispatcher.add_handler(set_webwork_password_handler)
  u.dispatcher.add_handler(help_handler)
  u.dispatcher.add_handler(notify_webwork_handler)
  u.start_polling()

if __name__ == '__main__':
  check.out1(3)
  main()