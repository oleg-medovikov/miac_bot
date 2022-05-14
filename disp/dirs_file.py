from .dispetcher import dp, bot
from aiogram import types
import pandas as pd, os
from clas import User, Dir

from aiogram.dispatcher.filters import BoundFilter

class IsDirsFile(BoundFilter):
    key = 'is_dirs_file'

    def __init__(self, is_dirs_file):
        self.is_dirs_file = is_dirs_file

    async def check(self, message: types.Message):

        USER = User(
                u_id = message['from']['id'],
                first_name = message['from']['first_name'],
                last_name = message['from']['last_name'],
                username = message['from']['username'],
                groups = '', fio ='', description = '',
                )
        if not message['document']['file_name'] == 'Dirs.xlsx':
            return False
        if not await USER.admin():
            await message.delete()
            return False
        return True


dp.filters_factory.bind(IsDirsFile)


@dp.message_handler(is_dirs_file=True, content_types=['document'])
async def update_dirs(message):
    FILE = message['document']
     
    DESTINATION = 'temp/' + FILE.file_unique_id + '.xlsx'
    await bot.download_file_by_id(
                file_id = FILE.file_id,
                destination = DESTINATION
                )
    
    await message.delete()

    COLUMNS = ['d_id','d_name','directory','description','working']
    TYPES = dict(
            d_id = int,
            d_name = str,
            directory = str,
            description = str,
            working = bool
            )

    try:
        df = pd.read_excel(DESTINATION, usecols=COLUMNS)
    except Exception as e:
        os.remove(DESTINATION)
        return await message.answer(str(e))
    
    ## Проверки файла на всякое
    # на наличие пустых ячеек
    if any(df.loc[df.isnull().to_numpy(),'d_id'] ):
        MESS = "Есть пустые ячейки! \n" \
                + str(df.loc[df.isnull().to_numpy(),'d_id'].unique())

        return await message.answer(MESS)

    df = df.astype(TYPES)
 
    
    # на уникальность d_id d_name

    if any(df['d_id'].duplicated()):
        MESS = "Повторяющиеся d_id: \n" \
                + str(df.loc[df['d_id'].duplicated(), 'd_id' ]) 
        
        return await message.answer(MESS)

    if any(df['d_name'].duplicated()):
        MESS = "Повторяющиеся d_name: \n" \
                + str(df.loc[df['d_name'].duplicated(), 'd_id' ]) 
        
        return await message.answer(MESS)



    for row in df.to_dict('records'):
        DIR = Dir(**row)
        await DIR.add()

    return await message.answer("Директории обновлены")


