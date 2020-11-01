import command_system
import db

def next(vk_id, body):
    candidates = db.get_candidates(vk_id)

    cand_keys = []
    for num, keys in enumerate(candidates):
        fullname = keys[0].lower() + ' ' + keys[1].lower() + ' ' + keys[2].lower()
        fullname = fullname.strip()
        cand_keys.append([fullname])
        cand_keys[num].append(keys[0].lower())
        cand_keys[num].append(str(num + 1) + '. ' + fullname)
        cand_keys[num].append(str(num + 1))
        cand_keys[num].append(str(num + 1) + '.')

        cand_keys[num].append(num)

    choice = None
    for cand in cand_keys:
        if body in cand:
            choice = cand[5]
            break

    if choice is None:
        return None, None


    db.make_choice(vk_id, candidates[choice][7])

    msg = 'Вы выбрали кандидата:\n'
    msg += str(choice + 1) + '. ' + candidates[choice][0] + ' ' + candidates[choice][1] + ' ' + candidates[choice][2] + '\n\n'

    if len(candidates) > 1:
        msg += 'Вы можете проголосовать одновременно ещё за других кандидатов:\n'

        for num, keys in enumerate(candidates):
            if num != choice:
                msg += str(num + 1) + '. ' + keys[0] + ' ' + keys[1] + ' ' + keys[2] + '\n'

        msg += '\nДля этого выберите кого-то из оставшихся кандидатов, либо отправьте его номер.\n\n'

        msg += 'Чтобы отменить выбор кандидата, нажмите на кнопку с ним повторно или отправьте его номер.\n\n'

        msg += 'Для того, чтобы завершить голосование, выберите соответствующий вариант, либо отправьте 0'

        return msg, '4.1'
    else:
        msg += 'Для того, чтобы подтвердить выбор, отправьте 0.\n\n'

        msg += 'Чтобы отменить выбор кандидата, нажмите на кнопку с ним повторно или отправьте его номер.'

        return msg, '4.1.1'

command_0 = command_system.Command(['4'])

command_0.description = 'Голосование'
command_0.process = next