from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file
from clas import Task

import pandas as pd
import os

@dp.message_handler(is_know=True, commands=['tasks', 'задачи'])
async def get_tasks(message: types.Message):
    U_ID = message['from']['id']
    df = pd.DataFrame( Task.get_all_tasks( U_ID ) )

    FILENAME = 'temp/Tasks.xlsx'
    SHETNAME = 'tasks'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.delete()
    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)

