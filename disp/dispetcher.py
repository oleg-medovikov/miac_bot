from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter
import logging


from conf import TELEGRAM_API
from clas import User 

logging.basicConfig(level=logging.INFO)
logging.getLogger('schedule').propagate = False
logging.getLogger('schedule').addHandler(logging.NullHandler())

bot = Bot(token=TELEGRAM_API)
dp  = Dispatcher(bot)



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
                groups = '', fio ='', description = '',
                )
        if not await USER.check():
            await USER.add_people() 
            try:
                await message.delete()
            except:
                pass
            await message.answer('Только для известных пользователей')
            return False
        else:
            return True

class IsAdmin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        USER = User(
                u_id = message['from']['id'],
                first_name = message['from']['first_name'],
                last_name = message['from']['last_name'],
                username = message['from']['username'],
                groups = '', fio ='', description = '',
                )
        if not await USER.admin():
            await message.delete()
            return False
        else:
            return True

dp.filters_factory.bind(IsKnown)
dp.filters_factory.bind(IsAdmin)

