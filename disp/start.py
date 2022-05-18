from .dispetcher import dp
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from func import hello_message
from clas import User

@dp.message_handler(is_know=True, commands=['start'])
async def send_welcome(message: types.Message):
    USER = await User.get_by_id( message['from']['id'] )

    try:
        await message.delete()
    except:
        pass

    res = await USER.access()

    if len(res):
        Choice = ReplyKeyboardMarkup(resize_keyboard=True)
        for command in res: 
            Choice.insert(KeyboardButton(text=command.c_name))
        
        await message.answer(hello_message(USER), parse_mode='html',reply_markup=Choice)
    else:
        mess = hello_message(USER) + '\n\n    Но у Вас пока нет доступных команд'
        await message.answer(mess, parse_mode='html')
        
    

