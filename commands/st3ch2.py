import command_system
import vkapi

def next(vk_id, body):

    keys = ['2. нет', '2.', '2', 'нет', 'неверно']
    if body in keys:
        vkapi.notify_admins('Данные избирателя не совпали!!! Избиратель: @id' + str(vk_id))
        return "Мы свяжемся с вами по поводу этого случая. Извините за неудобства!", '0.1'


    return None, None


command_0 = command_system.Command(['3'])

command_0.description = 'Неправильные данные'
command_0.process = next