from .dispetcher import dp, bot
from aiogram import types
import requests
from datetime import datetime
import pandas as pd

from clas import Task, User


@dp.message_handler(is_zam_stat=True, content_types=['text'] )
async def ask_log(message: types.Message):
    await message.delete()
    
    USER = User.get_by_id(message['from']['id'] )
    
    ACCESS = USER.access()

    TASK = Task(
        time_create = datetime.now(),
        client = message['from']['id'],
        task_type = 'Word_command',
        c_id = 48,
        c_func = 'zamechania_stat',
        c_arg = 'no',
        users_list = str( message['from']['id'] ),
        time_start = None,
        time_stop = None,
        comment = None
        )

    for t in ACCESS:
        if t['c_id'] == 48:
            return TASK.add()



