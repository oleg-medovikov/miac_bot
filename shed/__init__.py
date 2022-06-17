from .test_send import test_send
from .executor  import executor

import  asyncio, aioschedule

async def scheduler():
    aioschedule.every(10).seconds.do(executor)
    #aioschedule.every(1).minutes.do(test_send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

