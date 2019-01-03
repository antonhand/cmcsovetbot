import command_system
import db
import settings
import vkapi
import os

def next(vk_id, body):
    if vk_id not in settings.admin_ids:
        return None, None

    if not body.startswith("голоса"):
        return None, None

    res = db.get_results()

    msg = 'Номер,Выбор,Курс\n'


    for r in res:
        msg += ','.join(map(str, r)) + '\n'

    filename = "голоса.csv"

    f = open(filename, "w", encoding = "utf-8")

    print(msg, file = f)

    f.close()

    f = open(filename, "r", encoding = "utf-8")

    att = vkapi.upload_to_msg(vk_id, f)

    os.remove(filename)

    return "", att


command= command_system.AdmCommand()

command.description = 'Выгрузка голосов'
command.process = next