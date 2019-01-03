import command_system
import vkapi

def next(vk_id, body):
    keys = ['0. вернуться в главное меню', '0', '0.', 'вернуться в главное меню', 'вернуться', 'меню', 'вернуться в меню' ]
    if body in keys:
        return None, None

    vkapi.notify_admins("Сообщение Совету от пользователя @id" + str(vk_id))
    return "Спасибо за ваше сообщение!\nМы обязательно с вами свяжемся", '0'

command_0 = command_system.Command(['0.1'])

command_0.description = 'Отправить сообщение совету'
command_0.process = next