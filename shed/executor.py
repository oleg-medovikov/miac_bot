from disp import bot
from clas import Task, Command

import os, warnings

warnings.filterwarnings("ignore")

async def executor():
    TASK = Task.get()
    if TASK is None:
        return 1

    COMMAND = Command.get(TASK.c_id)


    try:
        return_value = await TASK.start()
    except Exception as e:
        # если функция сломалась
        TASK.comment = str(e)
        TASK.stop()
        return await bot.send_message(
                        TASK.client,
                        text=str(e),
                        parse_mode='html')
    else:
        #Если все хорошо, то получаем список, кому вернуть результат
        USERS = TASK.users()
        TASK.stop()
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

