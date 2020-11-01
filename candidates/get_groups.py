import command_system
import db
import settings
import vkapi
import os

def next(vk_id, body):
    if vk_id not in settings.cand_ids and vk_id not in settings.adm_ids:
        return None, None

    keys = ['по группам']
    if body not in keys:
        return None, None

    res = db.get_groups_stat()

    msg = 'Курс;Группа;Явка;Численность;Не голосовали\n'

    for r in res:
        if r[0] == 7:
            continue
        msg += ';'.join(map(str, r)) + '\n'

    filename = "явка по группам.csv"

    f = open(filename, "w", encoding = "utf-8")

    print(msg, file = f)

    f.close()

    f = open(filename, "r", encoding = "utf-8")

    att = vkapi.upload_to_msg(vk_id, f)

    os.remove(filename)

    return "", att


command = command_system.CandCommand()

command.description = 'Отобразить статистику'
command.process = next