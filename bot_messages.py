start_command_response =  "Привет, меня зовут Indigo!" \
                          "\n" \
                          "\n" \
                          "Я буду оповещать тебя о новых оценках, вебворках и буду подсказывать тебе расписание :)\n" \
                          "\n" \
                          "Пропиши /help, чтобы увидеть список доступных команд." \
                          "\n" \
                          "\n" \
                          "Удачи и высокого GPA!"

empty_login_response = "Логин не должен быть пустым :)"

updated_login_response = "Прекрасно, я обновил твой логин!"

empty_password_response = "Пароль не должен быть пустым :)"

updated_password_response = "Замечательно, я обновил твой пароль!"

new_webwork_response = "New webwork!\n"

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
                        "5. /notify_lectures - включение оповещений о лекциях заранее" \
                        "\n" \
                        "6. /next_lecture - увидеть следующую лекцию" \
                        "\n" \
                        "7. /set_webwork_password - обновление пароля от webwork'ов" \
                        "\n" \
                        "8. /notify_webwork - включение уведомлений о новых webwork'ах" \
                        "\n" \
                        "9. /help - список всех доступных команд"

no_login_or_password_response = 'Пожалуйста укажи свой логин и пароль. \n \nВведи /help, если понадобится помощь.'

checking_data_response = 'Один момент. Я проверю твои данные.'

wrong_webwork_data_response = 'Похоже ты ввел неправильные данные, или ты не зарегистрирован ни на один из курсов :('

wrong_registrar_data_response = 'Похоже ты ввел неправильные данные, попробуй обновить свой логин и пароль.'

successful_webwork_login_response = 'Отлично! Теперь я буду уведомлять тебя о новых вебворках.\nНа данный момент у тебя есть следующие открытые вебворки:'

successful_registrar_login_response = 'Круто! Я сохранил твое расписание, и теперь ты сможешь обращаться к нему в любой момент через команду /show_schedule ^_^'

no_schedule_response = 'У меня нет твоего расписания :(\n\nНе забудь указать свои данные, а затем вызвать /get_schedule, чтобы я сохранил твое расписание.'

wait_please_response = 'Так-с, подожди пару секунд..'

no_lectures_this_day = 'Нет лекций, ура! :)\n\n'

no_notifying_minutes_response = 'Количество минут должно быть от 1 до 120!'

notifying_minutes_not_number_response = 'Количество минут должно быть числом!'

successful_notifying_minutes_update_response = 'Найс! Теперь ты никогда не будешь опаздывать на уроки.'

set_username_response = 'Хорошо, приятель, какой у тебя логин? Не забудь про формат <b>name.surname</b>'

set_main_password_response = 'Ихихихи, мне нужен твой пароль, который ты используешь для входа в <b>registrar</b> и <b>moodle</b>. Обещаю его защищать :)'

set_webwork_password_response = 'Ух-ух, введи пароль, который ты используешь для входа в <b>webwork</b>. Обычно это твой Student ID.'

notify_lectures_response = 'Опаздываешь на лекции? Теперь не будешь :D\n\nВведи количество минут от 1 до 120, и я буду оповещать тебя о лекциях, когда до них останется количество минут, которое ты указал.'

going_to_another_command_response = 'Выполняю другую команду..'