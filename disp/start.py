from .dispetcher import dp
from aiogram import types

from func import hello_message
from clas import User

@dp.message_handler(is_know=True, commands=['start'])
async def send_welcome(message: types.Message):
    USER = await User.get_by_id( message['from']['id'] )

    try:
        await message.delete()
    except:
        pass
    await message.answer(hello_message(USER), parse_mode='html')
