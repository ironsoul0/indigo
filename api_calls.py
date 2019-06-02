import requests
import json
import os
from helpers import crypto

from cryptography.fernet import Fernet

from dotenv import load_dotenv
load_dotenv()

API_URL = os.environ['API_URL']
HEADERS = {
  'content-type': 'application/json; charset=utf-8'
}

def update_username(chat_id, new_username):
  payload = {
    'username': crypto.encrypt(new_username),
  }
  requests.post(
    '{}/chat/update_username/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=HEADERS
  )

def update_webwork_password(chat_id, new_password):
  payload = {
    'webwork_password': crypto.encrypt(new_password),
  }
  requests.post(
    '{}/chat/update_webwork_password/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=HEADERS
  )

def update_main_password(chat_id, new_password):
  payload = {
    'main_password': crypto.encrypt(new_password),
  }
  requests.post(
    '{}/chat/update_main_password/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=HEADERS
  )

def get_chat_info(chat_id):
  chat_info = requests.get(
    '{}/chat/{}'.format(API_URL, chat_id)
  )
  chat_info = json.loads(chat_info.text)
  return crypto.process_chat(chat_info)

def get_all_chats_info():
  result = requests.get(
    '{}/chat/all_chats'.format(API_URL)
  )
  result = json.loads(result.text)
  chats = result['chats']
  for i in range(0, len(chats)):
    chats[i] = crypto.process_chat(chats[i])
  return chats

def update_webworks_for_chat(chat_id, new_webworks):
  payload = {
    'new_webworks': crypto.encrypt(json.dumps(new_webworks))
  }
  requests.put(
    '{}/chat/update_webworks/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=HEADERS
  )

def update_schedule_for_chat(chat_id, new_schedule):
  payload = {
    'new_schedule': crypto.encrypt(json.dumps(new_schedule))
  }
  requests.put(
    '{}/chat/update_schedule/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=HEADERS
  )

def disable_notify_grades_for_chat(chat_id):
  requests.put(
    '{}/chat/disable_notify_grades/{}'.format(API_URL, chat_id)
  )

def update_grades_for_chat(chat_id, new_grades):
  payload = {
    'new_grades': crypto.encrypt(json.dumps(new_grades))
  }
  requests.put(
    '{}/chat/update_grades/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=HEADERS
  )

def update_schedule_notify_minutes(chat_id, new_minutes):
  payload = {
    'schedule_notify_minutes': new_minutes
  }
  requests.post(
    '{}/chat/update_schedule_notify_minutes/{}'.format(API_URL, chat_id),
    data=json.dumps(payload),
    headers=HEADERS
  )