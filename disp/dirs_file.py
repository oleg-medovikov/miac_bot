from .dispetcher import dp, bot
from aiogram import types
import pandas as pd, os
from clas import Dir

@dp.message_handler(is_admin=True, content_types=['document'])
async def update_dirs(message):
    print(1)
    FILE = message['document']
    if not FILE.file_name == 'Dirs.xlsx':
        return None
    
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


