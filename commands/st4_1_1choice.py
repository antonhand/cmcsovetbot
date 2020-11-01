import command_system
import db
import commands.st3ch1 as st3ch1
import commands.st4_1ch0 as st4_1ch0

def next(vk_id, body):
    candidates = db.get_candidates(vk_id)

    cand_keys = []
    for num, keys in enumerate(candidates):
        if keys[8]:
            fullname = keys[0].lower() + ' ' + keys[1].lower() + ' ' + keys[2].lower()
            fullname = fullname.strip()
            vars = [fullname]
            vars.append(str(num + 1) + '. ' + fullname)
            vars.append(str(num + 1))
            vars.append(str(num + 1) + '.')
            vars.append(keys[0].lower())
            vars.append(num)
            cand_keys.append(vars)

    choice = None
    for cand in cand_keys:
        if body in cand:
            choice = cand[5]
            break

    if choice is None:
        return None, None


    db.make_choice(vk_id, candidates[choice][7])

    candidates = db.get_candidates(vk_id)

    choosen = []

    not_choosen = []

    for num, cand in enumerate(candidates):
        fullname = cand[0] + ' ' + cand[1] + ' ' + cand[2]
        fullname = fullname.strip()
        if cand[8]:
            choosen.append(str(num + 1) + '. ' + fullname)
        else:
            not_choosen.append(str(num + 1) + '. ' + fullname)

    if choosen == []:
        return st3ch1.next(vk_id, '1')

    if not_choosen == []:
        return st4_1ch0.next(vk_id, '0')

    msg = 'Вы выбрали кандидатов:\n'

    for cand in choosen:
        msg += cand + '\n'

    msg += '\nВы также можете проголосовать и за других кандидатов:\n'

    for cand in not_choosen:
        msg += cand + '\n'

    msg += '\nДля этого выберите кого-то из оставшихся кандидатов, либо отправьте его номер.\n\n'

    msg += 'Чтобы отменить выбор кандидата, нажмите на кнопку с ним повторно или отправьте его номер.\n\n'

    msg += 'Для того, чтобы завершить голосование, выберите соответствующий вариант, либо отправьте 0'

    return msg, '4.1'


command_0 = command_system.Command(['4.1.1'])

command_0.description = 'Голосование'
command_0.process = next