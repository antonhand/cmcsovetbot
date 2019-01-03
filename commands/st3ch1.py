import command_system
import db

def next(vk_id, body):

    keys = ['1. да', '1.', '1', 'да']
    db.add_voter_num(vk_id)
    if body in keys:
        msg = 'На вашем курсе зарегистрированы следующие кандидаты:\n\n'

        candidates = db.get_candidates(vk_id)

        for num, cand in enumerate(candidates):
            if cand[4]:
                msg += str(num + 1) + '. @id' + str(cand[4]) + ' (' + cand[0] + ' ' + cand[1] + ' ' + cand[2] + ')\n'
            else:
                msg += str(num + 1) + '. ' + cand[0] + ' ' + cand[1] + ' ' + cand[2] + '\n'
            msg += 'Анкета: ' + cand[5] + '\n'

            if cand[6]:
                msg += 'Интервью: ' + cand[6] + '\n'

            msg += cand[3] + '\n\n'


        msg += 'Вы можете проголосовать за любое количество кандидатов\n\n'

        msg += 'Выберите кандидатов, за которых вы хотите проголосовать, либо отправьте их номера (по одному в сообщении).\n\n'

        msg += 'Вы также можете проголосовать против всех, отправив 0 (В этом случае вы голосуете за отказ от представительства курса в Студенческом совете)'

        return msg, '4'


    return None, None


command_0 = command_system.Command(['3'])

command_0.description = 'Данные избирателя верны'
command_0.process = next