import command_system
import db
import settings
import vkapi
import os

def next(vk_id, body):
    if vk_id not in settings.admin_ids:
        return None, None

    if not body.startswith("все избиратели"):
        return None, None

    res = db.get_all_voters()

    msg = 'ФИО,Дата голосования'



    year = None

    sp = body.split()

    if len(sp) > 2 and sp[2].isdigit():
        year = int(sp[2])

    if not year:
        msg += ',Курс\n'
    else:
        msg += '\n'

    for r in res:
        if year and r[2] != year:
            continue
        if year:
            msg += ','.join(map(str, r[:2])) + '\n'
        else:
            msg += ','.join(map(str, r)) + '\n'

    filename = "избиратели"

    if year:
        filename += " " + str(year) + " курс"

    filename += ".csv"

    f = open(filename, "w", encoding = "utf-8")

    print(msg, file = f)

    f.close()

    f = open(filename, "r", encoding = "utf-8")

    att = vkapi.upload_to_msg(vk_id, f)

    os.remove(filename)

    return "", att


command= command_system.AdmCommand()

command.description = 'Выгрузка всех проголосовавших'
command.process = next