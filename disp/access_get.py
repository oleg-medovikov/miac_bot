from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file
from base import POSTGRESS_EN

import pandas as pd
import os

@dp.message_handler(is_admin=True, commands=['access'])
async def get_access(message: types.Message):
    sql = """
    select a.u_id, u.fio, a.c_id, c.c_name, a.comment from access as a
        join users as u    on(u.u_id = a.u_id)
        join commands as c on(c.c_id = a.c_id)
        order by a.u_id, a.c_id
    """

    df = pd.read_sql(sql, POSTGRESS_EN )

    FILENAME = 'temp/Access.xlsx'
    SHETNAME = 'access'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.delete()
    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)


