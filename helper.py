from telegram.ext import Updater, CommandHandler
import requests
import re

def get_url():
	contents = requests.get('https://random.dog/woof.json').json()
	url = contents['url']
	return url

def bop(bot, update):
	url = get_url()
	chat_id = update.message.chat_id
	bot.send_photo(chat_id=chat_id, photo=url)

with requests.Session() as s:
	data = {
		'username': 'temirzhan.yussupov',
		'password': '515563515563aA',
		'rememberusername': '0'
	}
	p = s.post('https://moodle.nu.edu.kz/login/index.php', data=data)
	print(s.get('https://moodle.nu.edu.kz/course/user.php?mode=grade&id=903&user=2352').text)