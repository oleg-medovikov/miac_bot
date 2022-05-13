from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file
from base import POSTGRESS_EN

import pandas as pd
import os

@dp.message_handler(is_know=True, commands=['dirs'])
async def get_dirs(message: types.Message):
    df = pd.read_sql("select * from dirs", POSTGRESS_EN )

    FILENAME = 'temp/Dirs.xlsx'
    SHETNAME = 'dirs'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.delete()
    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)


