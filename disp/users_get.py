from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file
from clas import User
import pandas as pd
import os

@dp.message_handler(is_admin=True, commands=['users'])
async def get_users(message: types.Message):
    U_ID = message['from']['id']

    df = pd.read_sql( User.get_all( U_ID ))

    FILENAME = 'temp/Users.xlsx'
    SHETNAME = 'Users'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.delete()
    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)

