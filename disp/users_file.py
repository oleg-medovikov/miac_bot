from .dispetcher import dp, bot
from aiogram import types
import pandas as pd, os
from clas import User


from aiogram.dispatcher.filters import BoundFilter

class IsUsersFile(BoundFilter):
    key = 'is_users_file'

    def __init__(self, is_users_file):
        self.is_users_file = is_users_file

    async def check(self, message: types.Message):

        USER = User(
                u_id = message['from']['id'],
                first_name = message['from']['first_name'],
                last_name = message['from']['last_name'],
                username = message['from']['username'],
                groups = '', fio ='', description = '',
                )
        if not message['document']['file_name'] == 'Users.xlsx':
            return False
        if not USER.admin():
            await message.delete()
            return False
        return True

dp.filters_factory.bind(IsUsersFile)

@dp.message_handler(is_users_file=True, content_types=['document'])
async def update_users(message):
    U_ID = message['from']['id']
    FILE = message['document']
    
    DESTINATION = 'temp/' + FILE.file_unique_id + '.xlsx'
    await bot.download_file_by_id(
                file_id = FILE.file_id,
                destination = DESTINATION
                )
    
    await message.delete()

    COLUMNS = ['u_id','first_name','last_name',
               'username','groups','fio','description']
    TYPES = dict(
            u_id = int,
            first_name = str,
            last_name = str,
            username = str,
            groups = str,
            fio = str,
            description = str
            )

    try:
        df = pd.read_excel(DESTINATION, usecols=COLUMNS)
    except Exception as e:
        os.remove(DESTINATION)
        return await message.answer(str(e))
    
   
    ## Проверки файла на всякое
    # на наличие пустых ячеек
    if any(df.loc[df.isnull().to_numpy(),'u_id'] ):
        MESS = "Есть пустые ячейки! \n" \
                + str(df.loc[df.isnull().to_numpy(),'u_id'].unique())

        return await message.answer(MESS)

    df = df.astype(TYPES)
 
    # на уникальность c_id
    if any(df['u_id'].duplicated()):
        MESS = "Повторяющиеся u_id: \n" \
                + str(df.loc[df['u_id'].duplicated(), 'u_id' ]) 
        
        return await message.answer(MESS)

    # добавляем пользователей по одному
    for row in df.to_dict('records'):
        USER = User(**row)
        USER.add( U_ID )

    return await message.answer("Пользователи обновлены")


