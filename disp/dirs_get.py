from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file

from clas import Dir
import pandas as pd
import os

@dp.message_handler(is_know=True, commands=['dirs'])
async def get_dirs(message: types.Message):
    U_ID = message['from']['id']
    df = pd.DataFrame( data = Dir.get_all_dirs( U_ID ))

    FILENAME = 'temp/Dirs.xlsx'
    SHETNAME = 'dirs'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.delete()
    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)


