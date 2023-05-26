from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta
from uuid import uuid4, UUID

from conf import MIAC_API_URL, TOKEN
from base import t_tasks, t_users, t_commands, BASE
from sqlalchemy import select, desc

import requests


class my_except(Exception):
    pass


class Task(BaseModel):
    t_id:         UUID = Field(default_factory=uuid4)
    time_create:  datetime
    client:       int
    task_type:    str
    c_id:         int
    c_func:       str
    c_arg:        str
    users_list:   str
    time_start:   Optional[datetime]
    time_stop:    Optional[datetime]
    comment:      Optional[str]

    def add(self):
        """Создание нового задания
            Нужно проверить, есть ли в пуле 
            выполняющиеся такое задание"""
        HEADERS = dict(
            KEY = TOKEN,
            UID = str(self.client),
                )
        BODY = self.__dict__
        BODY['t_id'] = BODY['t_id'].hex
        BODY['time_create'] = BODY['time_create'].isoformat()

        URL = MIAC_API_URL + '/add_task'
        req = requests.post(URL, headers=HEADERS, json=BODY)
        return req.json()

    def get():
        """Взять доступную задачу"""
        HEADERS = dict(
            KEY = TOKEN
                )
        URL = MIAC_API_URL + '/get_task'
        req = requests.get(URL, headers=HEADERS)

        if not req.json() is None:
            return Task(**req.json())

    async def get_all():
        """Взять доступную задачу"""
        j = t_tasks.join(
            t_users,
            t_tasks.c.client == t_users.c.u_id,
            ).join(
            t_commands,
            t_tasks.c.c_id == t_commands.c.c_id,
            )
        query = select([
            t_tasks.c.time_create,
            t_users.c.fio,
            t_tasks.c.task_type,
            t_commands.c.c_name,
            t_tasks.c.c_arg,
            t_tasks.c.users_list,
            t_tasks.c.time_start,
            t_tasks.c.time_stop,
            t_tasks.c.comment,
            ]).order_by(desc(t_tasks.c.time_create)).select_from(j).where(
                t_tasks.c.time_create.between(
                    datetime.now() - timedelta(days=100),
                    datetime.now(),
                    ))

        res = await BASE.fetch_all(query)
        return [dict(r) for r in res]

    def restart():
        """Рестартануть выполнение задач, если бот перезапустился"""
        HEADERS = dict(
            KEY = TOKEN
                )
        URL = MIAC_API_URL + '/restart_tasks'
        req = requests.post(URL, headers=HEADERS)

    def stop(self):
        """Закончить задачу"""
        HEADERS = dict(
            KEY = TOKEN
                )
        BODY = self.__dict__

        try:
            BODY['t_id'] = BODY['t_id'].hex
        except:
            pass
        try:
            BODY['time_create'] = BODY['time_create'].isoformat()
        except:
            pass
        URL = MIAC_API_URL + '/stop_task'
        requests.post(URL, headers=HEADERS, json=BODY)

    def users(self):
        """Получить список юзеров для рассылки"""
        HEADERS = dict(
            KEY = TOKEN
                )
        BODY = self.__dict__
        BODY['t_id'] = BODY['t_id'].hex
        BODY['time_create'] = BODY['time_create'].isoformat()
        # BODY['time_start']  = BODY['time_start'].isoformat()
        URL = MIAC_API_URL + '/get_task_users_list'
        req = requests.get(URL, headers=HEADERS, json=BODY)

        return req.json()
