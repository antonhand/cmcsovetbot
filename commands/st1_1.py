import command_system
import db

def next(vk_id, body):
    if len(body.split()) < 2:
        return None, None

    vari = db.get_simular_voter_by_fn(body, vk_id, insert = True, is_self_named = True)

    if not vari:
        msg = 'Вы не найдены в наших списках. Проверьте, правильно ли ввели ваши ФИО и отправьте заново.'
        msg += 'Если вы уверены, что всё правильно, отправьте 1.\n\n'
        msg += 'Чтобы вернуться в главное меню, отправьте 0.\n\n'
        return msg, '1.1.1'

    msg = 'Пожалуйста, введите номер вашего студенческого билета (8 цифр), например 02191234.\n\n'

    msg += 'В случае, если вы ошиблись в выборе ФИО, отправьте 1\n\n'

    msg += 'Для возврата в главное меню отправьте 0.'

    return msg, '2'

command_0 = command_system.Command(['1.1'])

command_0.description = 'Ввод ФИО'
command_0.process = next