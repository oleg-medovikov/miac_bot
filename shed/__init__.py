from .test_send import test_send


import  asyncio, aioschedule

async def scheduler():
    #aioschedule.every(1).minutes.do(test_send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

