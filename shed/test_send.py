from disp import bot
from conf import CHAT_SVALKA_ID

async def test_send():
    await bot.send_message(chat_id=CHAT_SVALKA_ID, text='Ало!')


