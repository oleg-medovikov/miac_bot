from .dispetcher import dp, bot
from aiogram import types
import requests
from datetime import datetime
import pandas as pd

from clas import Task


@dp.message_handler(is_ask_log=True, content_types=['text'] )
async def ask_log(message: types.Message):
    COUNT = 20

    U_ID = message['from']['id']
    df = pd.DataFrame( Task.get_all_tasks( U_ID ) )

    IGNORE = ['Проверить ФР', 'Статус замечаний']

    df = df.loc[~df['c_name'].isin(IGNORE) ].head( COUNT )
   
    df['time_create'] = pd.to_datetime(df['time_create']).dt.strftime('%H:%M')
    
    df['delta'] = (pd.to_datetime(df['time_stop']) \
            - pd.to_datetime(df['time_start'])).dt.total_seconds().round(decimals=1)
    
    mess = f'```Последние {COUNT} выполненных задач:'
    mess += '\n' + '='*len(mess)

    _1 = df['fio'].str.len().max() 
    _2 = df['c_name'].str.len().max()


    for task in df.to_dict('records'):
        
        mess += '\n' + task['time_create'] +  ' | ' \
                + task['fio']    + ' '*(_1 - len(task['fio']) )     +  ' | ' \
                + task['c_name'] + ' '*(_2 - len(task['c_name']) )  +  ' | ' \
                + str(task['delta']) + ' сек.'
    

    mess += '```' 

    await message.delete()
    await message.answer(mess, parse_mode='Markdown')

