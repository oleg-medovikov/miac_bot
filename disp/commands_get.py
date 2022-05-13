from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file
from base import POSTGRESS_EN

import pandas as pd
import os

@dp.message_handler(is_admin=True, commands=['commands'])
async def get_commands(message: types.Message):
    df = pd.read_sql("select * from commands order by c_id", POSTGRESS_EN )

    FILENAME = 'temp/Commands.xlsx'
    SHETNAME = 'commands'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.delete()
    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)



