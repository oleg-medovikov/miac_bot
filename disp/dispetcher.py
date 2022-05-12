from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter
import logging

from conf import TELEGRAM_API
from base import POSTGRESS_DB
from func import set_default_commands
from clas import User 

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_API)
dp  = Dispatcher(bot)


async def on_startup(dp):
    await POSTGRESS_DB.connect()
    await set_default_commands(dp)


class IsKnown(BoundFilter):
    key = 'is_know'
    
    def __init__(self, is_know):
        self.is_know = is_know

    async def check(self, message: types.Message):
        USER = User(
                u_id = message['from']['id'],
                first_name = message['from']['first_name'],
                last_name = message['from']['last_name'],
                username = message['from']['username'],
                )
        if not await USER.check():
            await USER.add_people() 
            await message.answer('Только для известных пользователей')
            return False
        else:
            return True

dp.filters_factory.bind(IsKnown)

