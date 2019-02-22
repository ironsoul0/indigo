import requests
import json
import decrypter

API_URL = 'https://indigo-backend.herokuapp.com/chat'

def update_username(chat_id, new_username):
  payload = {
    'username': new_username,
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  requests.post(
    '{}/update_username/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )

def update_webwork_password(chat_id, new_password):
  payload = {
    'webwork_password': new_password,
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  requests.post(
    '{}/update_webwork_password/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )

def update_main_password(chat_id, new_password):
  payload = {
    'main_password': new_password,
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  requests.post(
    '{}/update_main_password/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )

def get_chat_info(chat_id):
  chat_info = requests.get(
    '{}/{}'.format(API_URL, chat_id)
  )
  chat_info = json.loads(chat_info.text)
  return decrypter.process_chat(chat_info)

def get_all_chats_info():
  result = requests.get(
    '{}/all_chats'.format(API_URL)
  )
  result = json.loads(result.text)
  chats = result['chats']
  for i in range(0, len(chats)):
    chats[i] = decrypter.process_chat(chats[i])
  return chats

def update_webworks_for_chat(chat_id, new_webworks):
  payload = {
    'new_webworks': new_webworks
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  requests.put(
    '{}/update_webworks/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )

def update_schedule_for_chat(chat_id, new_schedule):
  payload = {
    'new_schedule': new_schedule
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  requests.put(
    '{}/update_schedule/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )

def disable_notify_grades_for_chat(chat_id):
  return requests.put(
    '{}/disable_notify_grades/{}'.format(API_URL, chat_id)
  )

def update_grades_for_chat(chat_id, new_grades):
  payload = {
    'new_grades': new_grades
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  return requests.put(
    '{}/update_grades/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )

def update_schedule_notify_minutes(chat_id, new_minutes):
  payload = {
    'schedule_notify_minutes': new_minutes
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  requests.post(
    '{}/update_schedule_notify_minutes/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )