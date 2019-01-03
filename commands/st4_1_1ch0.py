import command_system
import db

def next(vk_id, body):

    keys = ['0. подтвердить', '0', '0.', 'подтвердить']
    if body in keys:
        db.confirm_votes(vk_id)

        voter_num = db.get_voter_num(vk_id)[0][0]

        msg = 'Спасибо за ваш голос!\n\n'

        msg += 'Ваш номер избирателя: ' + str(voter_num) + '\n\n'

        msg += 'По этому номеру вы сможете проверить, правильно ли учтён ваш голос. Информация с сопоставлением номеров избирателя и его голосов будет опубликована на нашей странице по завершении голосования.'

        return msg, '5'

    return None, None


command_0 = command_system.Command(['4.1.1'])

command_0.description = 'Неправильные данные'
command_0.process = next