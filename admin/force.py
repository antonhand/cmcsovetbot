import command_system
import vkapi
import settings
import messageHandler as mh

def next(vk_id, body):
    if vk_id not in settings.admin_ids:
        return None, None

    if not body.startswith("ответ "):
        return None, None

    spl = body.split()
    data = vkapi.get_last_msg(spl[1])
    mh.create_answer(data, settings.token)

    return "Выполнено", None


command= command_system.AdmCommand()

command.description = 'Ответить, если затык'
command.process = next