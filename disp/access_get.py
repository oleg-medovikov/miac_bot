from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file

import pandas as pd
import os

@dp.message_handler(is_admin=True, commands=['access'])
async def get_access(message: types.Message):
    U_ID = message['from']['id']

    df = pd.DataFrame(data = Access.get_all(U_ID) )

    FILENAME = 'temp/Access.xlsx'
    SHETNAME = 'access'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.delete()
    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)


