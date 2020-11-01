import command_system
import db
import settings

def next(vk_id, body):
    if vk_id not in settings.admin_ids:
        return None, None

    if not body.startswith("select"):
        return None, None

    res = db.select(body)

    return str(res), None


command= command_system.AdmCommand()

command.description = 'Селект'
command.process = next