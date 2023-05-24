from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file, delete_message
from clas import User
import pandas as pd
import os


@dp.message_handler(is_admin=True, commands=['users'])
async def get_users(message: types.Message):
    U_ID = message['from']['id']

    df = pd.DataFrame(User.get_all(U_ID))

    FILENAME = 'temp/Users.xlsx'
    SHETNAME = 'Users'

    write_styling_excel_file(FILENAME, df, SHETNAME)

    await delete_message(message)
    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)

