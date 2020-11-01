import command_system
import vkapi
import db
import keyboards as kb
import settings

def next(vk_id, body):
    if vk_id not in settings.admin_ids:
        return None, None

    if not body.startswith('/напомнить'):
        return None, None

    state = body.split()[1]

    msg = 'Добрый день!\n\n'

    msg += 'Вы не завершили авторизацию в боте. Для того, чтобы проголосовать, введите номер студенческого билета.'


    users = db.get_users_by_state(state)

    if users:
        vkapi.send_message_to_users(users, msg, keyboard = kb.get_board(state, '-1'))

    return 'Оповещено пользователей: ' + str(len(users)), None


command= command_system.AdmCommand()

command.description = 'Отправить приглашение'
command.process = next
