import command_system
import db

def next(vk_id, body):

    keys = ['0. завершить голосование', '0', '0.', 'завершить']
    if body in keys:
        msg = 'Вы выбрали кандидатов:\n'

        candidates = db.get_candidates(vk_id)

        for num, cand in enumerate(candidates):
            fullname = cand[0] + ' ' + cand[1] + ' ' + cand[2]
            fullname = fullname.strip()

            if cand[8]:
                msg += str(num + 1) + '. ' + fullname + '\n'

        msg += '\nДля того, чтобы подтвердить выбор, отправьте 0.\n\n'

        msg += 'Чтобы отменить выбор кандидата, нажмите на кнопку с ним повторно или отправьте его номер.'

        return msg, '4.1.1'

    return None, None


command_0 = command_system.Command(['4.1'])

command_0.description = 'Неправильные данные'
command_0.process = next