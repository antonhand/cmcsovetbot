import command_system
import db
import settings
import datetime

def next(vk_id, body):
    if vk_id not in settings.cand_ids and vk_id not in settings.adm_ids:
        return None, None

    keys = ['по потокам']
    if body not in keys:
        return None, None

    res = db.get_streams_stat()

    msg = 'На ' + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).strftime('%H:%M %d.%m.%Y') + ' явка по потокам составила:\n'

    for stream in res:
        if stream[0] == 7:
            continue
        msg += str(stream[0]) + ' курс ' + str(stream[1]) + " поток: " + str(stream[2]) + " из " +  str(stream[3]) + " -- " + ("%.2f" % (stream[2] / stream[3] * 100)).replace(".", ",") + "%\n"
        if stream[1] == 4 or stream[1] == 5:
            msg += '\n'

    return msg.replace("4 поток", "ФИИТ").replace("5 поток", "неинтегр."), None


command= command_system.CandCommand()

command.description = 'Отобразить статистику по потокам'
command.process = next