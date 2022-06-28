import asyncio, aioschedule
import datetime

from clas import Task
from conf import MASTER

async def scheduler():
    aioschedule.every().day.at('01:00').do( load_fr )
    aioschedule.every().day.at('02:00').do( load_fr )
    #aioschedule.every(1).minutes.do(test_send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def load_fr():
    TASK = Task(
        time_create = datetime.datetime.now(),
        client = MASTER,
        task_type = 'Sheduler',
        c_id = 41,
        c_func = 'load_fr',
        c_arg = 'no',
        users_list = str(MASTER),
        time_start = None,
        time_stop = None,
        comment = None
        )
    TASK.add()

async def load_fr_death():
    TASK = Task(
        time_create = datetime.datetime.now(),
        client = MASTER,
        task_type = 'Sheduler',
        c_id = 42,
        c_func = 'load_fr_death',
        c_arg = 'no',
        users_list = str(MASTER),
        time_start = None,
        time_stop = None,
        comment = None
        )
    TASK.add()
