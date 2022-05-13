from .dispetcher import dp
from aiogram import types

from func import hello_message, check_robot
from clas import User

@dp.message_handler(is_know=True, commands=['start'])
async def send_welcome(message: types.Message):
    USER = await User.get_by_id( message['from']['id'] )

    print(USER)

    await message.delete()
    await message.answer(hello_message(USER), parse_mode='html')
    await message.answer(await check_robot())
