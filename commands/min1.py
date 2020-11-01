import command_system
import vkapi
import settings

def next(vk_id, body):
    keys = ['начать', 'старт', 'start', 'голосовать', 'голос','выборы', 'привет']
    if body not in keys:
        return None, None

    name = vkapi.get_profile(vk_id)["first_name"]
    msg = 'Здравствуйте, ' + name + '!\n\n'

    if settings.close_years:
        years = set(settings.enable_years) - set(settings.close_years)
        msg += 'Если вы студент ВМК ' + ", ".join(map(str, years)) + ' курса, вы можете проголосовать на выборах в Студенческий совет ВМК.\n\n'
    else:
        msg += 'Если вы студент ВМК, вы можете проголосовать на выборах в Студенческий совет ВМК.\n\n'

    if settings.close_years:
        msg += 'Голосование на ' + ", ".join(map(str, settings.close_years)) + ' курсах завершено.\n\n'

    msg += 'Если вы хотите проголосовать, отправьте 1.\n\n'
    msg += 'Если вы хотите отправить сообщение в Студенческий совет ВМК, отправьте 2.'

    return msg, '0'

command_0 = command_system.Command(['-1', '0'])

command_0.description = 'Начать работу с ботом'
command_0.process = next