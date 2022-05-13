from .dispetcher import dp, bot
from aiogram import types
import pandas as pd, os
from clas import Command

@dp.message_handler(is_admin=True, content_types=['document'])
async def update_commands(message):
    FILE = message['document']
    if not FILE.file_name == 'Commands.xlsx':
        return None
    

    DESTINATION = 'temp/' + FILE.file_unique_id + '.xlsx'
    await bot.download_file_by_id(
                file_id = FILE.file_id,
                destination = DESTINATION
                )
    
    await message.delete()

    COLUMNS = ['c_id','c_category','c_name','c_procedure','c_arg','return_file','asc_day']
    TYPES = dict(
            c_id = int,
            c_category = str,
            c_name = str,
            c_procedure = str,
            c_arg = str,
            return_file = bool,
            asc_day = bool
            )

    try:
        df = pd.read_excel(DESTINATION, usecols=COLUMNS)
    except Exception as e:
        os.remove(DESTINATION)
        return await message.answer(str(e))
    
   
    ## Проверки файла на всякое
    # на наличие пустых ячеек
    if any(df.loc[df.isnull().to_numpy(),'c_id'] ):
        MESS = "Есть пустые ячейки! \n" \
                + str(df.loc[df.isnull().to_numpy(),'c_id'].unique())

        return await message.answer(MESS)

    df = df.astype(TYPES)
 
    
    # на уникальность c_id

    if any(df['c_id'].duplicated()):
        MESS = "Повторяющиеся c_id: \n" \
                + str(df.loc[df['c_id'].duplicated(), 'c_id' ]) 
        
        return await message.answer(MESS)

    # проверка на False True

    if df['return_file'].dtype != bool:
        MESS = "В колонке return_file есть неправильные значения!"

        return await message.answer(MESS)

    for row in df.to_dict('records'):
        COMMAND = Command(**row)
        await COMMAND.add()

    return await message.answer("Команды обновлены")



    

