from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID
from sqlalchemy import and_

from base import POSTGRESS_DB, t_tasks

class Task(BaseModel):
    t_id        : UUID = Field(default_factory=uuid4)
    time_create : datetime
    client      : int
    task_type   : str
    c_id        : int
    c_func      : str
    c_arg       : str
    users_list  : str
    time_start  : Optional[datetime]
    time_stop   : Optional[datetime]
    comment     : Optional[str]


    async def add(self):
        """Создание нового задания
            Нужно проверить, есть ли в пуле 
            выполняющиеся такое задание"""

        query = t_tasks.select(and_(
            t_tasks.c.time_stop == None,
            t_tasks.c.c_id == self.c_id
            ))
        res = await POSTGRESS_DB.fetch_one(query)

        if not res is None:
            if str(self.client) not in res['users_list']: 
                query = t_tasks.update()\
                        .where(t_tasks.c.t_id == res['t_id'])\
                        .values(users_list = res['users_list'] + ',' + str(self.client))
                await POSTGRESS_DB.execute(query)
        else:
            query = t_tasks.insert().values(self.__dict__)

            await POSTGRESS_DB.execute(query)

    async def get():
        """Взять доступную задачу"""
        query = t_tasks.select(t_tasks.c.time_start == None)

        res = await POSTGRESS_DB.fetch_one(query)
        
        if not res is None:
            query = t_tasks.update()\
                    .where(t_tasks.c.t_id == res['t_id'])\
                    .values(time_start = datetime.now())
            await POSTGRESS_DB.execute(query)
            return Task(**res)

    async def restart():
        """Рестартануть выполнение задач, если бот перезапустился"""
        query = t_tasks.update()\
                .where(t_tasks.c.time_stop == None)\
                .values(time_start = None )
        
        await POSTGRESS_DB.execute(query)

    async def stop(self):
        """Закончить задачу"""
        query =  t_tasks.update()\
                .where(t_tasks.c.t_id == self.t_id)\
                .values(time_stop = datetime.now(),
                        comment = self.comment)
        await POSTGRESS_DB.execute(query)

    async def users(self):
        """Получить список юзеров для рассылки"""
        query = t_tasks.select(t_tasks.c.t_id == self.t_id)

        res = await POSTGRESS_DB.fetch_one(query)
        
        if not res is None:
            list_ = [ int(x) for x in res["users_list"].split(',') ]
            return list_
