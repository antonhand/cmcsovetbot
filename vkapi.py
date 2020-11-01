import vk
import settings
import requests
import db
from datetime import date

session = vk.Session()
api = vk.API(session, v=settings.vk_api_ver)


def send_message(user_id, message, keyboard="", attachment="", random_id=0):
    if keyboard == "":
        api.messages.send(access_token=settings.token, user_id=str(user_id), message=message, attachment=attachment, dont_parse_links=settings.dont_parse_links)
    else:
        api.messages.send(access_token=settings.token, user_id=str(user_id), message=message, keyboard=keyboard, attachment=attachment, dont_parse_links=settings.dont_parse_links)

def send_message_to_users(users,  message, keyboard="", attachment=""):

    PACK_SIZE = 40

    for i in range(0, (len(users) - 1)//PACK_SIZE + 1):
        usrs = users[i * PACK_SIZE:min(len(users), (i + 1) * PACK_SIZE)]
        if keyboard == "":
            api.messages.send(access_token=settings.token, user_ids=usrs, random_id=0, message=message, attachment=attachment, dont_parse_links=settings.dont_parse_links)
        else:
            api.messages.send(access_token=settings.token, user_ids=usrs, random_id=0, message=message, keyboard=keyboard, attachment=attachment, dont_parse_links=settings.dont_parse_links)


def get_profile(user_id):
    res = api.users.get(user_ids=user_id, access_token=settings.token)

    return res[0]

def notify_admins(message):
    for user_id in settings.admin_ids:
        api.messages.send(access_token=settings.token, user_id=str(user_id), random_id=0, message=message)


def get_potential_users():
    active_users = db.get_active_users()
    users = []
    again = True
    offset = 0
    while again:
        msgs = api.messages.getConversations(access_token = settings.token, offset = offset, count = 200)['items']
        offset += 200
        for msg in msgs:
            conv = msg['conversation']
            user_id = conv['peer']['id']
            if user_id in active_users:
                continue

            last = msg['last_message']

            if date.fromtimestamp(last['date']) < date.fromisoformat('2017-01-01'):
                again = False
                continue

            users.append(user_id)

    return users

def upload_to_msg(vk_id, file):
    url = api.docs.getMessagesUploadServer(access_token=settings.token, peer_id = vk_id)
    url = url["upload_url"]

    ftype = ""

    sp = file.name.split(".")

    if len(sp) > 0:
        ftype = "." + sp.pop()

    r = requests.post(url, files = {"file": ("upl" + ftype, file)})

    servfile = r.json()["file"]

    res = api.docs.save(access_token=settings.token, file = servfile, title = file.name)

    res = res[0]


    return "doc" +  str(res["owner_id"]) + "_" + str(res["id"])

def get_last_msg(vk_id):
    res = api.messages.getHistory(access_token=settings.token, count = 1, user_id = vk_id)
    res = res["items"][0]
    return res