start_command_response =  "Привет 👋🏼, меня зовут Indigo!" \
                          "\n" \
                          "\n" \
                          "Я буду оповещать тебя о новых оценках, вебворках и буду подсказывать тебе расписание 😋\n" \
                          "\n" \
                          "Пропиши /help, чтобы увидеть список доступных команд." \
                          "\n" \
                          "\n" \
                          "Удачи и высокого GPA!"
                          
empty_login_response = "Логин не должен быть пустым :)"

updated_login_response = "Прекрасно, я обновил твой логин!"

empty_password_response = "Пароль не должен быть пустым :)"

updated_password_response = "Замечательно, я обновил твой пароль!"

new_webwork_response = "Новый webwork!\n\n"

unknown_command_response = "Прости, но я не знаю эту команду.\nВведи /help, чтобы увидеть список доступных команд."

help_command_response = "Доступные команды:" \
                        "\n" \
                        "\n" \
                        "1. /set_username - обновление логина" \
                        "\n" \
                        "2. /set_main_password - обновление пароля для входа в moodle и registrar" \
                        "\n" \
                        "3. /get_schedule - сохранить расписание" \
                        "\n" \
                        "4. /show_schedule - показать расписание" \
                        "\n" \
                        "5. /notify_grades - включение уведомлений о новых оценках" \
                        "\n" \
                        "6. /notify_lectures - включение оповещений о лекциях заранее" \
                        "\n" \
                        "7. /next_lecture - увидеть следующую лекцию" \
                        "\n" \
                        "8. /set_webwork_password - обновление пароля от webwork'ов" \
                        "\n" \
                        "9. /notify_webwork - включение уведомлений о новых webwork'ах" \
                        "\n" \
                        "10. /feedback - сообщить о баге, предложить новый функционал" \
                        "\n" \
                        "11. /help - список всех доступных команд"

no_login_or_password_response = 'Пожалуйста укажи свой логин и пароль. \n \nВведи /help, чтобы увидеть команды при помощи которых это можно сделать.'

no_webwork_login_or_password_response = 'Пожалуйста укажи свой логин и пароль для входа в <b>webwork</b>. \n \nИспользуй команды /set_username и /set_webwork_password.'

checking_data_response = 'Один момент. Я проверю твои данные.'

wrong_webwork_data_response = 'Похоже ты ввел неправильные данные, или ты не зарегистрирован ни на один из курсов :('

wrong_registrar_data_response = 'Похоже ты ввел неправильный логин или пароль, либо у тебя нет расписания на текущий семестр.'

wrong_moodle_data_response = 'Похоже у тебя нет курсов на текущий семестр, либо ты ввел неправильный логин или пароль. Попробуй обновить их и попробовать снова.'

wrong_login_response = 'Введенный логин не соответсвует формату <b>name.surname</b>. Попробуй ввести логин еще раз.'

successful_webwork_login_response = 'Отлично! Теперь я буду уведомлять тебя о новых вебворках.\nНа данный момент у тебя есть следующие открытые вебворки:'

successful_registrar_login_response = 'Круто! Я сохранил твое расписание, и теперь ты сможешь обращаться к нему в любой момент через команду /show_schedule 😸'

successful_moodle_login_response = 'Замечательно! Теперь я буду уведомлять тебя о новых оценках!'

no_schedule_response = 'У меня нет твоего расписания :(\n\nНе забудь указать свои данные, а затем вызвать /get_schedule, чтобы я сохранил твое расписание.'

no_lectures_this_day = 'Нет лекций, ура! 😝\n\n'

no_notifying_minutes_response = 'Количество минут должно быть от 0 до 120!'

notifying_minutes_not_number_response = 'Количество минут должно быть числом!'

successful_notifying_minutes_update_response = 'Кул! Теперь ты никогда не будешь опаздывать на уроки.'

set_username_response = 'Хорошо, приятель, какой у тебя логин для входа в <b>registrar</b> и <b>moodle</b>? Это строка формата <b>name.surname</b> (например, <b>dastan.bakubaev</b>)\n\nВведи /cancel, если вызвал команду по ошибке.'

set_main_password_response = 'Введи пароль, который ты используешь для входа в <b>registrar</b> и <b>moodle</b>. Все пароли надежно шифруются, поэтому можешь не беспокоится за их сохранность.\n\nВведи /cancel, если вызвал команду по ошибке.'

set_webwork_password_response = 'Так-с, введи пароль, который ты используешь для входа в <b>webwork</b>. Обычно это твой Student ID.\n\nВведи /cancel, если вызвал команду по ошибке.'

notify_lectures_response = 'Опаздываешь на лекции? Теперь не будешь 😝\n\nВведи количество минут от 1 до 120, и я буду оповещать тебя о лекциях, когда до них останется количество минут, которое ты указал.\n\nВведи 0, если хочешь, чтобы я перестал оповещать тебя о предстоящих лекциях.\n\nВведи /cancel, если вызвал команду по ошибке.'

feedback_command_response = 'Напишите Ваш отзыв, мы обязательно его прочтем 👻\n\nПропишите /cancel, если вызвали команду по ошибке.'

disable_notifying_minutes_response = 'Больше не буду уведмолять тебя о предстоящих лекциях 🙂'

going_to_another_command_response = '🐶'

password_changed_response = 'Похоже ты поменял пароль. Если да, то пожалуйста вызови /set_main_password, а после /notify_grades.'

command_cancel_response = 'Команда отменена 😌'

full_grade = 'Отличная работа!'

almost_full_grade = 'Супер! Давай в том же духе ✊'

feedback_sent_response = 'Ваш отзыв отправлен! Спасибо за обратную связь 😉'