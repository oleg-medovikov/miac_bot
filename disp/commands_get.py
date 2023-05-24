from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file, delete_message

from clas import Command
import pandas as pd
import os


@dp.message_handler(is_admin=True, commands=['commands'])
async def get_commands(message: types.Message):
    U_ID = message['from']['id']
    df = pd.DataFrame(data=Command.get_all(U_ID))

    FILENAME = 'temp/Commands.xlsx'
    SHETNAME = 'commands'

    write_styling_excel_file(FILENAME, df, SHETNAME)

    await delete_message(message)
    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)
