from func import set_default_commands
from .dispetcher import dp
from clas import Task
from shed import scheduler
from base import POSTGRESS_DB
import asyncio

async def on_startup(dp):
    await POSTGRESS_DB.connect()
    await Task.restart()
    await set_default_commands(dp)
    asyncio.create_task(scheduler())

