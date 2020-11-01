import command_system
import vkapi
import db

def next(vk_id, body):
    prof = vkapi.get_profile(vk_id)
    name = prof["first_name"]
    surname = prof["last_name"]
    vari = db.get_simular_voter(name, surname, vk_id)

    max_num = len(vari) + 1

    keys = [str(max_num), str(max_num) + '.', str(max_num) + '. меня нет в списке', 'нет в списке']

    if body in keys:
        db.delete_vars(vk_id)
        msg = 'Введите ваши Фамилию Имя Отчество, например, Иванов Иван Иванович\n\n'

        msg += 'Для возврата в главное меню отправьте 0.'

        return msg, '1.1'

    var_keys = []
    for num, keys in enumerate(vari):
        var_keys.append([keys[0].lower()])
        var_keys[num].append(str(num + 1))
        var_keys[num].append(str(num + 1) + '.')
        var_keys[num].append(str(num + 1) + '. ' + keys[0].lower())
        label = str(num + 1) + '. ' + keys[0].lower()
        if len(label) > 40:
            label = label[:37] + "..."
        var_keys[num].append(label)

    choice = None
    for v in var_keys:
        if body in v:
            choice = v[0]
            break

    if not choice:
        return None, None

    db.delete_vars(vk_id, except_fn = choice)

    msg = 'Пожалуйста, введите номер вашего студенческого билета (8 цифр), например 02551234.\n\n'

    msg += 'Номер студенческого расположен так, как это показано на картинке (vk.com/photo-115682804_457239596). Не путайте с номером читательского билета, который тоже иногда вносят в студенческий сбоку.\n\n'

    msg += 'В случае, если вы ошиблись в выборе ФИО, отправьте 1\n\n'

    msg += 'Для возврата в главное меню отправьте 0.'

    return msg, '2'

command_0 = command_system.Command(['1'])

command_0.description = 'Выбор варианта ФИО'
command_0.process = next