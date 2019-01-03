import vkapi
import os
import importlib
from command_system import command_list, adm_com_list
import db
import keyboards as kb
import settings

def load_modules():
    files = os.listdir("mysite/commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("commands." + m[:-3])
    files = os.listdir("mysite/admin")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("admin." + m[:-3])


def get_answer(body, vk_id):
    state = db.get_state(vk_id)
    att = None
    message = "Неверный ввод. Попробуйте ещё раз"
    next_state = state
    notify = False
    if state == '-1':
        notify = True
        name = vkapi.get_profile(vk_id)["first_name"]
        message = 'Здравствуйте, ' + name + '!\n'
        message += 'Спасибо за ваше сообщение! Мы обязательно ответим на него чуть позже.\n\n'
        message += 'На данный момент проходят Дистанционные выборы в Студенческий совет ВМК. Если вы студент ВМК, вы можете проголосовать прямо здесь\n\n'
        years = set(settings.enable_years) - set(settings.close_years)
        message += 'Голосование доступно для' + ", ".join(map(str, years)) + ' курса, для 2 курса магистратуры, к сожалению, голосование недоступно, т.к. на курсе не зарегистрировался ни один кандидат.\n\n'
        if settings.close_years:
            message += 'Голосование на ' + ", ".join(map(str, settings.close_years)) + ' курсах завершено.\n\n'
        message += 'Если вы хотите проголосовать, отправьте 1.\n\n'
        message += 'Если вы хотите отправить ещё одно сообщение в Студенческий совет ВМК, отправьте 2.'
        next_state = '0'

    if state in command_list.keys():
        for com in command_list[state]:
            msg, nxt_state = com.process(vk_id, body)
            if msg is not None:
                message = msg
                next_state = nxt_state
                notify = False
                break
    else:
        message =  None
        next_state = None

    if not message and vk_id in settings.admin_ids:
        for com in adm_com_list:
            msg, att = com.process(vk_id, body)
            if msg is not None:
                message = msg
                next_state = state
                notify = False
                break

    if notify:
        vkapi.notify_admins("Сообщение Совету от пользователя @id" + str(vk_id))
        vkapi.notify_admins("Текст:\n" + body)
    return message, next_state, kb.get_board(next_state, vk_id), att

def create_answer(data, token):
    load_modules()

    vk_id = data['from_id']

    if settings.is_test and vk_id not in settings.test_users:
        return

    message, next_state, keyboard, att = get_answer(data['text'].lower(), vk_id)
    if not message and not att:
        return
    vkapi.send_message(vk_id, message, keyboard, att)
    db.set_state(vk_id, next_state)