from disp import dp, on_startup
from aiogram import executor
from shed import scheduler
import warnings, asyncio

warnings.filterwarnings("ignore")

async def main():
    await asyncio.gather(
        on_startup(dp),
        scheduler(),
    )


#from multiprocessing import Process
#async def main():
#    Process(target= on_startup, args=(dp ), daemon=False).start()
#    Process(target= scheduler, args=(), daemon=False).start()

from threading import Thread

def bot_tread():
    asyncio.create_task( on_startup(dp) )
def scheduler_tread():
    asyncio.create_task( scheduler )


if __name__ == '__main__':
    '''
    Thread(
            name='miac_bot',
            target=bot_tread,
            daemon=False
            ).start()

    Thread(
            name='scheduler',
            target=scheduler_tread,
            daemon=False
            ).start()
    '''
    asyncio.run(main())

