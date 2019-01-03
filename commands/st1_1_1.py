import commands.st1_1 as st1_1
import command_system
import vkapi

def next(vk_id, body):
    keys = ['1. фио введены верно', '1.', '1', 'верно', 'всё верно']
    if body in keys:
        vkapi.notify_admins('ФИО избирателя не найдены в списках. Избиратель: @id' + str(vk_id))
        return "Мы свяжемся с вами по поводу этого случая. Извините за неудобства!", '0.1'

    ret = st1_1.next(vk_id, body)
    if ret[0]:
        return ret
    return None, None

command_0 = command_system.Command(['1.1.1'])

command_0.description = 'Повторная попытка ввода ФИО'
command_0.process = next