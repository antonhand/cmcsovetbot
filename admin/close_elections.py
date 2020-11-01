'''import command_system
import vkapi
import db
import settings

def next(vk_id, body):
    if vk_id not in settings.admin_ids:
        return None

    keys = ['/закрыть!']
    if body not in keys:
        return None,

    users = db.get_not_finalized_voters()

    for us in users:
        msg = 'Добрый день!\n\n'
        msg += 'Голосование на выборах завершено.\n'
        msg += 'Вы не завершили голосование, т.к. не выбрали ни одного варианта или не подтвердили свой выбор, поэтому признаётесь воздержавшимся при голосовании.\n\n'
        msg += 'Ваш номер избирателя ' + str(us[1])+ '\n\n'
        msg += 'По этому номеру вы сможете проверить, правильно ли учтён ваш голос. Информация с сопоставлением номеров избирателя и его голосов будет опубликована на нашей странице по завершении подсчёта голосов.'

        vkapi.send_message(us[0], msg)

        db.set_state(us[0], '6')



    return 'Оповещено пользователей: ' + str(len(users)), None


command= command_system.AdmCommand()

command.description = 'Заввершит ьголосование и разослать воздержавшимся номера.'
command.process = next'''