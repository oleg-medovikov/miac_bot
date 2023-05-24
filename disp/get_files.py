from .dispetcher import dp
from aiogram import types

from func import write_styling_excel_file, delete_message
from clas import User, Command, Access, Dir

import pandas as pd
import os

COMMANDS = [
    'access',
    'dirs',
    'users',
    'commands',
]


@dp.message_handler(commands=COMMANDS)
async def get_files(message: types.Message):
    await delete_message(message)
    U_ID = message['from']['id']
    COMMAND = message.text.replace('/', '')
    if not await User.admin(U_ID):
        return message.answer('Нет прав для этой операции')

    JSON = {
        'access':   Access.get_all(),
        'dirs':     Dir.get_all(),
        'users':    User.get_all(),
        'commands': Command.get_all(),

    }.get(COMMAND)

    df = pd.DataFrame(data=await JSON)

    FILENAME = f'/tmp/{COMMAND}.xlsx'
    SHETNAME = COMMAND

    write_styling_excel_file(FILENAME, df, SHETNAME)

    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)
