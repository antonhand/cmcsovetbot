import command_system
import vkapi

def next(vk_id, body):

    keys = ['1. номер студбилета введён верно', '1.', '1', 'верно', 'всё верно']
    if body in keys:
        vkapi.notify_admins('Номер студбилета избирателя не совпал с данными для ФИО. Избиратель: @id' + str(vk_id))
        return "Мы свяжемся с вами по поводу этого случая. Извините за неудобства!", '0.1'


    return None, None


command_0 = command_system.Command(['2.1'])

command_0.description = 'Ошибка в вводе номера студбилета'
command_0.process = next