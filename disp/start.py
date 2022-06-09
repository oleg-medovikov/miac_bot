from .dispetcher import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData
import uuid, datetime, time, os, asyncio

from func import hello_message
from clas import User, Command, Task, Choice

command = CallbackData('post','id', 'action' )

asyncio.set_event_loop(asyncio.new_event_loop()) 
LOOP = asyncio.get_event_loop()


@dp.message_handler(is_know=True, commands=['start', 'старт'])
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
        # Если нужно спросить день, посылаем календарь
        CHOICE = Choice(u_id = U_ID, c_id = COMMAND.c_id)
        await CHOICE.add()
        await query.message.delete()
        await bot.send_message(
                U_ID,
                text="Выбор даты:",
                reply_markup=await SimpleCalendar().start_calendar())
        
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
        if await TASK.add():
            await query.answer(
                    'Задача добавлена, ожидайте результата',
                    show_alert=False)
            try:
                await query.message.delete()
            except:
                pass
           
            return LOOP.create_task(background_task(TASK, COMMAND) )

            #await asyncio.to_thread(background_task, TASK, COMMAND)
            #loop = asyncio.get_running_loop()
            #await loop.run_in_executor(None, background_task, TASK, COMMAND)
            
            #await asyncio.create_subprocess_exec(background_task,TASK, COMMAND)
            
            #await background_task(TASK, COMMAND)

        else:
            # Если команда уже создана и выполняется
            await query.answer(
                    'Команда уже запущена другим пользователем, ожидайте ответ',
                    show_alert=False)
            try:
                await query.message.delete()
            except:
                pass

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
    
    await callback_query.message.answer(f'Для команды "{COMMAND.c_name}" выбрана дата {date.strftime("%d.%m.%Y")}' )

    if await TASK.add():
        await query.answer(
                'Задача добавлена, ожидайте результата',
                show_alert=False)
        try:
            await query.message.delete()
        except:
            pass
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.ensure_future(background_task(loop,TASK, COMMAND))

    else:
        # Если команда уже создана и выполняется
        await query.answer(
                'Команда уже запущена другим пользователем, ожидайте ответ',
                show_alert=False)
        try:
            await query.message.delete()
        except:
            pass




async def background_task(TASK : Task, COMMAND : Command):
    print(1)
    try:
        return_value = await TASK.start()
    except Exception as e:
        # если функция сломалась
        TASK.comment = str(e)
        await TASK.stop()
        return await bot.send_message(
                        TASK.client,
                        text=str(e),
                        parse_mode='html')
    else:
        #Если все хорошо, то получаем список, кому вернуть результат
        USERS = await TASK.users()
        await TASK.stop()
        #Возвращаем результат
            
        if COMMAND.return_file:
            for FILE in return_value.split(';'):
                for USER in USERS:
                    await bot.send_document(
                            chat_id=USER,
                            document=open(FILE, 'rb'))
                os.remove(FILE)
        else:
            for USER in USERS:
                await bot.send_message(chat_id=USER, text=return_value)
