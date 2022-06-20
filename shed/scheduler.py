from .executor import executor
import  asyncio, aioschedule

async def scheduler():
    aioschedule.every(2).seconds.do(executor)
    #aioschedule.every(1).minutes.do(test_send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

