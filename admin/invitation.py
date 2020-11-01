import command_system
import vkapi
import db
import keyboards as kb
import settings

def next(vk_id, body):
    if vk_id not in settings.admin_ids:
        return None, None

    if not body.startswith('/пригласить'):
        return None, None

    year = body.split()[1]

    msg = 'Добрый вечер!\n\n'

    msg += 'В прошлом году вы голосовали здесь на выборах в Студсовет.\n'
    msg += 'В этом году мы приглашаем снова проголосовать за представителей вашего курса.\n\n'
    msg += 'Для вас процедура авторизации в боте упрощена -- вам не придётся вводить ФИО и номер студенческого!\n\n'
    msg += 'Если вы хотите проголосовать, отправьте 1.\n\n'
    msg += 'Если вы хотите отправить сообщение в Студенческий совет ВМК, отправьте 2.'


    users = db.get_prev_novote_users(year)

    if users:
        vkapi.send_message_to_users(users, msg, keyboard = kb.get_board('0', '-1'))

    return 'Оповещено пользователей: ' + str(len(users)), None


command= command_system.AdmCommand()

command.description = 'Отправить приглашение'
command.process = next




'''import command_system
import vkapi
import db
import keyboards as kb
import settings

def next(vk_id, body):
    if vk_id not in settings.admin_ids:
        return None

    keys = ['/оповестить!']
    if body not in keys:
        return None,

    msg = 'Добрый день!\n\n'
    msg += 'Вы не закончили процесс голосования.\n'
    msg += 'Меньше суток осталось до завершения выборов. Вы всё ещё можете проголосовать здесь.\n\n'
    msg += 'Если у вас возникли какие-то затруднения, вы можете написать @anton.hand (Антону) и мы решим проблему.\n\n'


    users = db.get_users_by_state('2')

    if users:
        vkapi.send_message_to_users(users, msg, keyboard = kb.get_board('2', '-1'))

    return 'Оповещено пользователей: ' + str(len(users)), None


command= command_system.AdmCommand()

command.description = 'Отправить приглашение'
command.process = next'''