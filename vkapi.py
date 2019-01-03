import vk
import settings
import requests
import db
from datetime import date

session = vk.Session()
api = vk.API(session, v=5.87)


def send_message(user_id, message, keyboard="", attachment=""):
    if keyboard == "":
        api.messages.send(access_token=settings.token, user_id=str(user_id), message=message, attachment=attachment, dont_parse_links=1)
    else:
        api.messages.send(access_token=settings.token, user_id=str(user_id), message=message, keyboard=keyboard, attachment=attachment, dont_parse_links=1)

def send_message_to_users(users,  message, keyboard="", attachment=""):
    for i in range(0, (len(users) - 1)//100 + 1):
        usrs = users[i * 100:min(len(users), (i + 1) * 100)]
        if keyboard == "":
            api.messages.send(access_token=settings.token, user_ids=usrs, message=message, attachment=attachment, dont_parse_links=1)
        else:
            api.messages.send(access_token=settings.token, user_ids=usrs, message=message, keyboard=keyboard, attachment=attachment, dont_parse_links=1)


def get_profile(user_id):
    get_param = {}
    get_param["user_ids"] = user_id
    get_param["access_token"] = settings.token
    get_param["v"] = "5.87"

    response = requests.get('https://api.vk.com/method/users.get', params = get_param).json()

    return response["response"][0]

def notify_admins(message):
    for user_id in settings.admin_ids:
        api.messages.send(access_token=settings.token, user_id=str(user_id), message=message)


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