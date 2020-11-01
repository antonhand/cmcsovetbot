import command_system
import vkapi
import db
import settings

def next(vk_id, body):
    if vk_id not in settings.admin_ids:
        return None, None

    if body != '/предупредить':
        return None, None


    if settings.remind:
        return None, None

    settings.remind = True

    msg = 'Добрый день!\n\n'

    msg += 'Вы не завершили голосование.\n'
    msg += 'Для того, чтобы завершить голосование, необходимо выбрать всех кандидатов, за которых вы хотите проголосовать, и подтвердить ваш выбор. После этого вам будет выдан номер избирателя.\n\n'
    msg += 'Сегодня пройдёт подведение итогов выборов на вашем курсе. Пользователи, которые не завершат голосование, будут признаны воздержавшимися при голосовании.'

    users = db.get_not_finalized_voters()

    if users:
        vkapi.send_message_to_users(users, msg)

    return 'Оповещено пользователей: ' + str(len(users)), None

command= command_system.AdmCommand()

command.description = 'Отправить приглашение'
command.process = next
