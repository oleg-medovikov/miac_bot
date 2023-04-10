from .dispetcher import dp, bot
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from datetime import datetime
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from func import hello_message
from clas import User, Command, Task, Choice

command = CallbackData('post', 'id', 'action')


@dp.message_handler(is_know=True, commands=['start', 'старт'])
async def send_welcome(message: types.Message):
    USER = User.get_by_id(message['from']['id'])

    try:
        await message.delete()
    except:
        pass

    res = USER.access()
    if len(res):

        Choice = types.InlineKeyboardMarkup(
                resize_keyboard=True,
                row_width=2
                )

        for com in res:
            if com['asc_day']:
                ACTION = 'Ask day'
            else:
                ACTION = 'No ask day'

            Choice.insert(types.KeyboardButton(
                text=com['c_name'],
                callback_data=command.new(id=com['c_id'], action=ACTION)
                ))

        await message.answer(
                hello_message(USER),
                parse_mode='html',
                reply_markup=Choice)
    else:
        mess = hello_message(USER) \
                + '\n\n    Но у Вас пока нет доступных команд'
        await message.answer(mess, parse_mode='html')


@dp.callback_query_handler(command.filter())
async def standart_command_handler(
        query: types.CallbackQuery,
        callback_data: dict):
    """обработка комманд без даты в аргументе"""
    U_ID = query['from']['id']

    COMMAND = Command.get(callback_data['id'])

    if COMMAND.asc_day:
        # Если нужно спросить день, посылаем календарь
        CHOICE = Choice(u_id=U_ID, c_id=COMMAND.c_id)
        CHOICE.add()
        await query.message.delete()
        await bot.send_message(
                U_ID,
                text="Выбор даты:",
                reply_markup=await SimpleCalendar().start_calendar(
                    datetime.now().year,
                    datetime.now().month
                    ))

    else:
        TASK = Task(
                # t_id = str(uuid.uuid4()),
                time_create=datetime.now(),
                client=int(U_ID),
                task_type='Command',
                c_id=COMMAND.c_id,
                c_func=COMMAND.c_procedure,
                c_arg=COMMAND.c_arg,
                users_list=U_ID,
                time_start=None,
                time_stop=None,
                comment=None
                )

        res = TASK.add()
        await query.answer(res['mess'], show_alert=False)

        try:
            await query.message.delete()
        except:
            pass


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(
        callback_query: types.CallbackQuery,
        callback_data: dict):
    """Создание задания после выбора даты из календаря"""

    selected, date = await SimpleCalendar().process_selection(
            callback_query,
            callback_data)

    if selected:
        U_ID = callback_query['from']['id']
        C_ID = Choice.get(U_ID)
        COMMAND = Command.get(C_ID)

        if COMMAND.c_arg == 'no':
            C_ARG = date.strftime("%d-%m-%Y")
        else:
            C_ARG = date.strftime("%d-%m-%Y") + ';' + COMMAND.c_arg

        TASK = Task(
                # t_id=str(uuid.uuid4()),
                time_create=datetime.now(),
                client=int(U_ID),
                task_type='Command',
                c_id=COMMAND.c_id,
                c_func=COMMAND.c_procedure,
                c_arg=C_ARG,
                users_list=U_ID,
                time_start=None,
                time_stop=None,
                comment=None
                )

    TASK.add()
    MESS = f"""Для команды '{COMMAND.c_name}'
    выбрана дата {date.strftime("%d.%m.%Y")}"""
    await callback_query.message.answer(MESS)
