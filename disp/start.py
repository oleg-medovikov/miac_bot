from .dispetcher import dp
from aiogram import types

from func import hello_message, check_robot
from clas import User

@dp.message_handler(is_know=True, commands=['start'])
async def send_welcome(message: types.Message):
    USER = User(
                u_id = message['from']['id'],
                first_name = message['from']['first_name'],
                last_name = message['from']['last_name'],
                username = message['from']['username'],
                )
    

    await message.delete()
    await message.answer(hello_message(USER), parse_mode='html')
    await message.answer(await check_robot())
