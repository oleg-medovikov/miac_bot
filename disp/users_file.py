from .dispetcher import dp, bot
from aiogram import types
import pandas as pd, os
from clas import User

@dp.message_handler(is_admin=True, content_types=['document'])
async def update_users(message):
    FILE = message['document']
    if not FILE.file_name == 'Users.xlsx':
        return None
    
    DESTINATION = 'temp/' + FILE.file_unique_id + '.xlsx'
    await bot.download_file_by_id(
                file_id = FILE.file_id,
                destination = DESTINATION
                )
    
    await message.delete()

    COLUMNS = ['u_id','first_name','last_name','username','groups','fio','description']
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


    for row in df.to_dict('records'):
        USER = User(**row)
        await USER.add()

    return await message.answer("Пользователи обновлены")


