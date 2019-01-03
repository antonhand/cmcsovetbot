import command_system
import db
import commands.st0ch1 as st0ch1

def next(vk_id, body):

    keys = ['2', '2.', '2. вернуться к выбору фио', 'фио']

    if body in keys:
        if db.is_self_named(vk_id):
            db.delete_vars(vk_id)
            msg = 'Введите ваши Фамилию Имя Отчество, например, Иванов Иван Иванович\n\n'

            msg += 'Для возврата в главное меню отправьте 0.'

            return msg, '1.1'
        else:
            return st0ch1.next(vk_id, '1')

    return None, None


command_0 = command_system.Command(['2.1'])

command_0.description = 'Возврат к выбору ФИО'
command_0.process = next