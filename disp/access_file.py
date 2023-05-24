from .dispetcher import dp, bot
from aiogram import types
import pandas as pd
import os
from clas import User, Access

from func import delete_message
from aiogram.dispatcher.filters import BoundFilter


class IsAccessFile(BoundFilter):
    key = 'is_access_file'

    def __init__(self, is_access_file):
        self.is_access_file = is_access_file

    async def check(self, message: types.Message):

        USER = User(
                u_id=message['from']['id'],
                first_name=message['from']['first_name'],
                last_name=message['from']['last_name'],
                username=message['from']['username'],
                groups='', fio='', description='',
                )
        if not message['document']['file_name'] == 'Access.xlsx':
            return False
        if not USER.admin():
            await delete_message(message)
            return False
        return True


dp.filters_factory.bind(IsAccessFile)


@dp.message_handler(is_access_file=True, content_types=['document'])
async def update_access(message):
    FILE = message['document']
    U_ID = message['from']['id']
    DESTINATION = 'temp/' + FILE.file_unique_id + '.xlsx'

    await bot.download_file_by_id(
                file_id=FILE.file_id,
                destination=DESTINATION
                )

    await delete_message(message)

    COLUMNS = ['u_id', 'c_id', 'comment']

    TYPES = dict(
            u_id=int,
            c_id=int,
            comment=str,
            )

    try:
        df = pd.read_excel(DESTINATION, usecols=COLUMNS)
    except Exception as e:
        os.remove(DESTINATION)
        return await message.answer(str(e))

    # Проверки файла на всякое
    # на наличие пустых ячеек
    if any(df.loc[df.isnull().to_numpy(), 'u_id']):
        MESS = "Есть пустые ячейки! \n" \
                + str(df.loc[df.isnull().to_numpy(), 'c_id'].unique())

        return await message.answer(MESS)

    df = df.astype(TYPES)

    # удаляем полностью все допуски
    Access.delete_all(U_ID)

    # добавляем обратно построчно
    for row in df.to_dict('records'):
        ACCESS = Access(**row)
        ACCESS.add(U_ID)

    return await message.answer("Допуски обновлены")
