from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file
from base import POSTGRESS_EN
from clas import User

import pandas as pd
import os

@dp.message_handler(is_know=True, commands=['tasks', 'задачи'])
async def get_tasks(message: types.Message):
    USER = await User.get_by_id(message['from']['id'])
    if await USER.admin():
        sql = """
        select
            t.time_create
            ,u.fio
            ,t.task_type
            ,c.c_name
            ,t.c_arg
            ,t.users_list
            ,t.time_start
            ,t.time_stop
            ,t.comment
        from tasks as t
            join users as u  on(u.u_id = t.client)
            join commands as c on(c.c_id = t.c_id)
            order by t.time_create desc"""
    else:
        sql = f"""
        select
            t.time_create
            ,u.fio
            ,t.task_type
            ,c.c_name
            ,t.c_arg
            ,t.users_list
            ,t.time_start
            ,t.time_stop
            ,t.comment
        from tasks as t
            join users as u  on(u.u_id = t.client)
            join commands as c on(c.c_id = t.c_id)
        where t.client = {USER.u_id}
        order by t.time_create desc
            """

    df = pd.read_sql(sql, POSTGRESS_EN )

    FILENAME = 'temp/Tasks.xlsx'
    SHETNAME = 'tasks'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.delete()
    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)

