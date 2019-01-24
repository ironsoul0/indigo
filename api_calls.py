import requests
import json

API_URL = 'https://nu-bot-backend.herokuapp.com/chat'

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
  return json.loads(chat_info.text)

def get_all_chats_info():
  result = requests.get(
    '{}/all_chats'.format(API_URL)
  )
  result = json.loads(result.text)
  return result['chats']

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