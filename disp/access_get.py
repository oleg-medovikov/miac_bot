from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file, delete_message
from clas import Access

import pandas as pd
import os


@dp.message_handler(is_admin=True, commands=['access'])
async def get_access(message: types.Message):

    await delete_message(message)
    JSON = await Access.get_all()

    df = pd.DataFrame(data=JSON)

    FILENAME = 'temp/Access.xlsx'
    SHETNAME = 'access'

    write_styling_excel_file(FILENAME, df, SHETNAME)

    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)
