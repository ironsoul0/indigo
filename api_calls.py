import requests
import json
import decrypter
import os

API_URL = ''

try:
  import sensitive
  API_URL = sensitive.API_URL
except ImportError:
  API_URL = os.environ['API_URL']
  print(API_URL)

def update_username(chat_id, new_username):
  payload = {
    'username': new_username,
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  requests.post(
    '{}/chat/update_username/{}'.format(API_URL, chat_id),
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
    '{}/chat/update_webwork_password/{}'.format(API_URL, chat_id),
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
    '{}/chat/update_main_password/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )

def get_chat_info(chat_id):
  chat_info = requests.get(
    '{}/chat/{}'.format(API_URL, chat_id)
  )
  chat_info = json.loads(chat_info.text)
  return decrypter.process_chat(chat_info)

def get_all_chats_info():
  result = requests.get(
    '{}/chat/all_chats'.format(API_URL)
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
    '{}/chat/update_webworks/{}'.format(API_URL, chat_id),
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
    '{}/chat/update_schedule/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )

def disable_notify_grades_for_chat(chat_id):
  return requests.put(
    '{}/chat/disable_notify_grades/{}'.format(API_URL, chat_id)
  )

def update_grades_for_chat(chat_id, new_grades):
  payload = {
    'new_grades': new_grades
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  return requests.put(
    '{}/chat/update_grades/{}'.format(API_URL, chat_id),
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
    '{}/chat/update_schedule_notify_minutes/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=headers
  )

def get_room_participants(room_id="5c9f1ba989811004cdb5014c"):
  payload = {
    'room_id': room_id
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  result = requests.get(
    '{}/room/get_participants'.format(API_URL),
    data=json.dumps(payload),
    headers=headers
  )
  result = json.loads(result.text)
  return result['participants']

def toggle_room_participant(chat_id, room_id="5c9f1ba989811004cdb5014c"):
  payload = {
    'chat_id': chat_id,
    'room_id': room_id
  }
  headers = {
    'content-type': 'application/json; charset=utf-8'
  }
  requests.post(
    '{}/room/toggle_participant'.format(API_URL),
    data=json.dumps(payload),
    headers=headers
  )