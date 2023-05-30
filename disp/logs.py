from .dispetcher import dp
from aiogram import types
import pandas as pd

from clas import Task
from func import delete_message


@dp.message_handler(is_ask_log=True, content_types=['text'])
async def ask_log(message: types.Message):
    COUNT = 20
    await delete_message(message)

    df = pd.DataFrame(await Task.get_log(COUNT))

    # IGNORE = ['Проверить ФР', 'Статус замечаний']
    # df = df.loc[~df['c_name'].isin(IGNORE)].head(COUNT)

    df['fio'] = df['fio'].str.split(' ', n=0, expand=True)
    df['time_create'] = pd.to_datetime(df['time_create']).dt.strftime('%H:%M')

    df['delta'] = (
            pd.to_datetime(df['time_stop']) - pd.to_datetime(df['time_start'])
        ).dt.total_seconds().round(decimals=1)

    mess = f'``` Последние {COUNT} выполненных задач:'
    mess += '\n' + '='*len(mess)

    _1 = df['fio'].str.len().max()
    # _2 = df['c_name'].str.len().max()

    for task in df.to_dict('records'):
        mess += '\n' + task['time_create'] + ' | ' \
                + task['fio'] + ' '*(_1 - len(task['fio'])) + ' | ' \
                + task['c_name'][:13] \
                + ' '*(13 - len(task['c_name'][:13])) + ' | ' \
                + str(task['delta']) + ' с.'
        # + task['c_name'][:13] + ' '*(_2 - len(task['c_name']) )  +  ' | ' \

    mess += '```'

    await message.answer(mess, parse_mode='Markdown')
