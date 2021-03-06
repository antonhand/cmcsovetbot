import command_system
import db
import re

def next(vk_id, body):

    if body in ('1', '2'):
        return None, None


    if not re.match("^[0-9]+$", body.strip()):
        return None, None

    studnum = 0
    try:

        studnum = int(body)
        if len(body) not in range(7,9):
            return 'В номере студенческого должно быть 8 цифр', '2'
    except Exception:
        return None, None

    studnum_res = db.check_studnum(vk_id, studnum)

    if studnum_res[0] == 'end':
        msg = 'У вас есть три неудачные попытки!\n\n'

        msg += 'По закону может быть не более двух пересдач!\n\n'

        msg += 'К сожалению, ничего сделать не можем. Вынуждены представить вас к участию в очных выборах на вашем курсе.'

        return msg, '2.1.1'

    if studnum_res[0] == 'already':
        msg = 'Cтудент уже вошёл в систему под другим пользователем ВКонтакте\n\n'
        msg += 'Данная активность является подозрительной, дальнейшая работа с ботом для вашего пользователья заблокирована\n\n'
        msg += 'Если вы считаете, что это ошибка, напишите нам'
        return msg, '0.1'

    if studnum_res[0] == 'good':
        db.delete_vars(vk_id)
        msg = 'Ваши данные\n'
        msg += 'ФИО: ' + studnum_res[1][0] + '\n'
        msg += 'Курс: ' + str(studnum_res[1][1]) + '\n\n'

        msg += 'Всё верно?\n\n'
        msg += 'Отправьте 1, если да, отправьте 2, если нет.'

        return msg, '3'


    msg = 'Номер билета не соответствует вашим данным. Проверьте, правильно ли ввели ваш и отправьте заново.\n\n'

    if studnum_res[1] == 0:
        msg += 'По закону может быть не более двух пересдач!\n'
        msg += 'У вас осталось 2 попытки ввести номер студенческого билета.\n\n'
    else:
        msg += 'У вас осталась 1 попытка ввести номер студенческого билета.\n\n'

    msg += 'Если вы нашли ошибку, введите номер студенческого билета правильно.\n\n'

    msg += 'Если вы уверены, что всё правильно, отправьте 1.\n\n'

    msg += 'Если вы неправильно ввели свои ФИО, отправьте 2.\n\n'

    msg += 'Для возврата в главное меню отправьте 0.'

    return msg, '2.1'

command_0 = command_system.Command(['2', '2.1'])

command_0.description = 'Ввод  номера студенческого билета'
command_0.process = next