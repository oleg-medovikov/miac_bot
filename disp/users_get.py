from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file
from base import POSTGRESS_EN

import pandas as pd
import os

@dp.message_handler(is_admin=True, commands=['users'])
async def get_users(message: types.Message):
    df = pd.read_sql("select * from users order by u_id", POSTGRESS_EN )

    FILENAME = 'temp/Users.xlsx'
    SHETNAME = 'Users'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.delete()
    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)


