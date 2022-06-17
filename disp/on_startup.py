from func import set_default_commands
from .dispetcher import dp
from clas import Task
from shed import scheduler

import asyncio

async def on_startup(dp):
    Task.restart()
    await set_default_commands(dp)
    while True:
        try:
            await dp.start_polling()
        except:
            asyncio.sleep(5)

