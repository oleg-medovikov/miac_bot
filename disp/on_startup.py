from func import set_default_commands
from .dispetcher import dp
from shed import scheduler
from base import POSTGRESS_DB
import asyncio

async def on_startup(dp):
    await POSTGRESS_DB.connect()
    asyncio.create_task(scheduler())
    await set_default_commands(dp)


