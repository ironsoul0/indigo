from telegram.ext import CommandHandler 

response_text = (
  "Доступные команды:\n\n"
  "1. /set_username - обновление логина\n" 
  "2. /set_main_password - обновление пароля для входа в moodle и registrar\n" 
  "3. /get_schedule - сохранить расписание\n" 
  "4. /show_schedule - показать расписание\n"
  "5. /notify_grades - включение уведомлений о новых оценках\n" 
  "6. /notify_lectures - включение оповещений о лекциях заранее\n" 
  "7. /next_lecture - увидеть следующую лекцию\n" 
  "8. /set_webwork_password - обновление пароля от webwork'ов\n" 
  "9. /notify_webwork - включение уведомлений о новых webwork'ах\n" 
  "10. /feedback - сообщить о баге, предложить новый функционал\n" 
  "11. /help - список всех доступных команд"
)

def handler(update, context):
  update.message.reply_text(response_text)

help_handler = CommandHandler('help', handler)