import command_system
import commands.st3ch1 as st3ch1

def next(vk_id, body):

    keys = ['0. вернуться к выбору кандидатов', '0', '0.', 'вернуться']
    if body in keys:
        return st3ch1.next(vk_id, '1')

    return None, None


command_0 = command_system.Command(['4.2'])

command_0.description = 'Неправильные данные'
command_0.process = next