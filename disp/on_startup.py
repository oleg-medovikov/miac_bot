from func import set_default_commands
from clas import Task

import asyncio


async def on_startup(dp):
    Task.restart()
    await set_default_commands(dp)
    while True:
        try:
            await dp.start_polling()
        except Exception as e:
            print(str(e))
            asyncio.sleep(5)
