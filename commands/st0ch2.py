import command_system

def next(vk_id, body):

    keys = ['2. отправить сообщение студсовету', '2', '2.', 'отправить сообщение студсовету', 'сообщение', 'отправить']
    if body in keys:
        return 'Вводите сообщение. Для возврата в главное меню, введдите 0', '0.1'

    return None, None

command_0 = command_system.Command(['0'])

command_0.description = 'Отправить сообщение Совету'
command_0.process = next