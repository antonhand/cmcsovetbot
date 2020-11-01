import command_system
import vkapi
import db

def next(vk_id, body):
    keys = ['1. проголосовать на выборах', '1', '1.', 'проголосовать на выборах', 'проголосовать на выборах', 'проголосовать']
    if body not in keys:
        return None, None

    prev_user = db.get_prev_user(vk_id)

    if prev_user:
        msg = 'Ваши данные\n'
        msg += 'ФИО: ' + prev_user[0] + '\n'
        msg += 'Курс: ' + str(prev_user[1]) + '\n\n'

        msg += 'Всё верно?\n\n'
        msg += 'Отправьте 1, если да, отправьте 2, если нет.'

        return msg, '3'


    prof = vkapi.get_profile(vk_id)
    name = prof["first_name"]
    surname = prof["last_name"]
    vari = db.get_simular_voter(name, surname, vk_id, insert=True)
    msg = ''
    new_state = '1'



    if vari:
        msg = 'Для голосования необходимо представиться. Возможно, вы кто-то из перечисленных людей?\n\n'
        for num, keys in enumerate(vari):
            msg += str(num + 1) + '. ' + keys[0] + '\n'
        msg += str(len(vari) + 1) + '. Меня нет в списке\n\n'
        msg += 'Выберите правильный вариант или отправьте его номер.\n\n'
        msg += 'Для возврата в главное меню отправьте 0.'
        new_state = '1'
    else:
        msg = 'Для голосования необходимо представиться.\n'
        msg += 'Введите, пожалуйста, ваши Фамилию Имя Отчество, например, Иванов Иван Иванович\n\n'
        msg += 'Для возврата в главное меню отправьте 0.'
        new_state = '1.1'

    return msg, new_state

command_0 = command_system.Command(['0'])

command_0.description = 'Проголосовать на выборах'
command_0.process = next