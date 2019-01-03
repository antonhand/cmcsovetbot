import command_system
import db
import settings
import datetime
import math

def next(vk_id, body):
    if vk_id not in settings.admin_ids:
        return None, None

    keys = ['по курсам']
    if body not in keys:
        return None, None

    res = db.get_stat()

    msg = 'На ' + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%H:%M %d.%m.%Y') + ' явка составила:\n'

    for year in res:
        if year[0] == 7:
            continue
        msg += str(year[0]) + ' курс: ' + str(year[1]) + " из " + str(year[2]) + " -- " + ("%.2f" % (year[1] / year[2] * 100)).replace(".", ",") + "%, до кворума: " + str(math.ceil(year[2]/2) - year[1]) + "\n"

    return msg, None


command= command_system.AdmCommand()

command.description = 'Отобразить статистику'
command.process = next