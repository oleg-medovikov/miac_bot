from disp import bot

from clas import Task, Command
from func import *

from concurrent.futures import ThreadPoolExecutor
import os

async def executor():
    TASK = await Task.get()
    if TASK is None:
        return 1
   
    COMMAND = await Command.get(TASK.c_id)

    # Запускаем новый тред с процедурой
    with ThreadPoolExecutor() as executor:
        if TASK.c_arg == 'no':
            future = executor.submit(globals()[COMMAND.c_procedure])
        else:
            future = executor.submit(globals()[COMMAND.c_procedure],TASK.c_arg)
        try:
            return_value = await future.result()
        except Exception as e:
            # если что-то поломалось то заканчиваем задачу с ошибкой в комментарии
            TASK.comment = str(e)
            await TASK.stop()
            await bot.send_message(TASK.client, text=str(e), parse_mode='html')
            return 1
        else:
            # Получаем список,кому вернуть результат
            USERS = await TASK.users()
            # Возвращаем результат

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
        
            await TASK.stop()


