from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
import uuid, datetime, time

from func import hello_message
from clas import User, Command, Task

command = CallbackData('post','id', 'action')

@dp.message_handler(is_know=True, commands=['start'])
async def send_welcome(message: types.Message):
    USER = await User.get_by_id( message['from']['id'] )

    try:
        await message.delete()
    except:
        pass

    res = await USER.access()
    
    if len(res):

        Choice = types.InlineKeyboardMarkup(resize_keyboard=True)
        for com in res: 

            Choice.insert(types.KeyboardButton(
                text = com.c_name,
                callback_data = command.new(id = USER.u_id, action = com.c_id)  ))
        
        await message.answer(hello_message(USER), parse_mode='html',reply_markup=Choice)
    else:
        mess = hello_message(USER) + '\n\n    Но у Вас пока нет доступных команд'
        await message.answer(mess, parse_mode='html')


@dp.callback_query_handler(command.filter())
async def some_callback_handler(query: types.CallbackQuery, callback_data: dict):

    COMMAND = await Command.get(callback_data['action'])
    TASK = Task(
            t_id = uuid.uuid4(),
            time_create = datetime.datetime.now(),
            client = int(callback_data['id']),
            task_type = 'Command',
            c_id = COMMAND.c_id,
            c_func = COMMAND.c_procedure,
            c_arg = COMMAND.c_arg,
            users_list = callback_data['id'],
            time_start = None,
            time_stop = None,
            comment = None
            )
    await TASK.add()
    await query.answer('Задача добавлена, ожидайте результата', show_alert=False)
    time.sleep(2)
    await query.message.delete()

