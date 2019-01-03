
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, json
import settings
import messageHandler
import vkapi

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from you!'

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys() :
        return 'not vk'

    if 'secret' not in data.keys():
        return 'not enough'

    if data['secret'] != settings.secret:
        return 'go home'

    if data['type'] == 'confirmation':
        return settings.confirmation_token
    elif data['type'] == 'message_new':
        try:
            messageHandler.create_answer(data['object'], settings.token)
            return 'ok'
        except Exception as e:
            vkapi.notify_admins('Бот упал...')
            vkapi.notify_admins(str(e))
            raise e