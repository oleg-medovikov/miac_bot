from .dispetcher import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
import uuid, datetime, time

from func import hello_message
from clas import User, Command, Task, Choice

command = CallbackData('post','id', 'action' )

@dp.message_handler(is_know=True, commands=['start'])
async def send_welcome(message: types.Message):
    USER = await User.get_by_id( message['from']['id'] )

    try:
        await message.delete()
    except:
        pass

    res = await USER.access()
    
    if len(res):

        Choice = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)

        for com in res: 
            if com.asc_day:
                ACTION = 'Ask day'
            else:
                ACTION = 'No ask day'

            Choice.insert(types.KeyboardButton(
                text = com.c_name,
                callback_data = command.new(id = com.c_id, action = ACTION )  ))
        
        await message.answer(hello_message(USER), parse_mode='html',reply_markup=Choice)
    else:
        mess = hello_message(USER) + '\n\n    Но у Вас пока нет доступных команд'
        await message.answer(mess, parse_mode='html')

from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar


## обработка комманд без даты в аргументе
@dp.callback_query_handler(command.filter())
async def standart_command_handler(query: types.CallbackQuery, callback_data: dict):
    U_ID = query['from']['id']
    
    COMMAND = await Command.get(callback_data['id'])

    if COMMAND.asc_day:
        CHOICE = Choice(u_id = U_ID, c_id = COMMAND.c_id)
        await CHOICE.add()
        await query.message.delete()
        await bot.send_message(U_ID, text="Выбор даты:", reply_markup=await SimpleCalendar().start_calendar())
        
    else:
        TASK = Task(
                t_id = uuid.uuid4(),
                time_create = datetime.datetime.now(),
                client = int(U_ID),
                task_type = 'Command',
                c_id = COMMAND.c_id,
                c_func = COMMAND.c_procedure,
                c_arg = COMMAND.c_arg,
                users_list = U_ID,
                time_start = None,
                time_stop = None,
                comment = None
                )
        await TASK.add()
        await query.answer('Задача добавлена, ожидайте результата', show_alert=False)
        time.sleep(2)
        await query.message.delete()

        await query.answer('Задача добавлена, ожидайте результата', show_alert=False)

## Создание задания после выбора даты из календаря
@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        U_ID    = callback_query['from']['id']
        C_ID    = await Choice.get(U_ID)
        COMMAND = await Command.get(C_ID)

        TASK = Task(
                t_id = uuid.uuid4(),
                time_create = datetime.datetime.now(),
                client = int(U_ID),
                task_type = 'Command',
                c_id = COMMAND.c_id,
                c_func = COMMAND.c_procedure,
                c_arg = date.strftime("%d-%m-%Y"),
                users_list = U_ID,
                time_start = None,
                time_stop = None,
                comment = None
                )
        await TASK.add()

        await callback_query.message.answer(f'Для команды "{COMMAND.c_name}" выбрана дата {date.strftime("%d.%m.%Y")}' )

