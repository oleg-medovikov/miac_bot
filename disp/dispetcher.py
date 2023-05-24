from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import BoundFilter
import logging

from conf import TELEGRAM_API
from clas import User
from func import delete_message

logging.basicConfig(level=logging.INFO)
logging.getLogger('schedule').propagate = False
logging.getLogger('schedule').addHandler(logging.NullHandler())

bot = Bot(token=TELEGRAM_API)
dp = Dispatcher(bot)


class IsKnown(BoundFilter):
    key = 'is_know'

    def __init__(self, is_know):
        self.is_know = is_know

    async def check(self, message: types.Message):
        USER = User(
                u_id=message['from']['id'],
                first_name=message['from']['first_name'],
                last_name=message['from']['last_name'],
                username=message['from']['username'],
                groups='', fio='', description='',
                )
        if not USER.check():
            # USER.add_people()
            await delete_message(message)
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
                u_id=message['from']['id'],
                first_name=message['from']['first_name'],
                last_name=message['from']['last_name'],
                username=message['from']['username'],
                groups='', fio='', description='',
                )
        if not USER.admin():
            await delete_message(message)
            return False
        else:
            return True


class IsAskLog(BoundFilter):
    key = 'is_ask_log'

    def __init__(self, is_ask_log):
        self.is_ask_log = is_ask_log

    async def check(self, message: types.Message):

        if message['text'] in ('?', 'log', 'лог'):
            return True
        else:
            return False


class IsZamStat(BoundFilter):
    key = 'is_zam_stat'

    def __init__(self, is_zam_stat):
        self.is_zam_stat = is_zam_stat

    async def check(self, message: types.Message):

        if message['text'] in ('zam', 'зам', 'замечания'):
            return True
        else:
            return False


dp.filters_factory.bind(IsKnown)
dp.filters_factory.bind(IsAdmin)
dp.filters_factory.bind(IsAskLog)
dp.filters_factory.bind(IsZamStat)
