import command_system
import db

def next(vk_id, body):
    keys = ['0. вернуться в главное меню', '0', '0.', 'вернуться в главное меню', 'вернуться', 'меню', 'вернуться в меню' ]
    if body not in keys:
        return None, None
    db.delete_vars(vk_id)
    msg = 'Вы можете проголосовать на выборах в Студенческий совет ВМК.\n\n'
    msg += 'Если вы хотите проголосовать, отправьте 1.\n\n'
    msg += 'Если вы хотите отправить сообщение в Студенческий совет ВМК, отправьте 2.'

    return msg, '0'

command_0 = command_system.Command(['0.1', '1', '1.1', '1.1.1', '2', '2.1'])

command_0.description = 'Вернуться в меню'
command_0.process = next